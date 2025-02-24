from data_storing.DataReader import DataReader
from ImageDisplayer import ImageDisplayer
from TensorflowModelTest import TensorflowModelTest
from ImageManipulator import ImageManipulator
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt

THRESHOLD = 0.9

d = DataReader()
m = ImageManipulator()
model = TensorflowModelTest('contrast_model/v0_contrast.h5')

# Bild laden
image, _ = d.read("990.h5", "train_images")
image = image / 255.0
original_image = image.copy()

# Helligkeit berechnen
height, width = original_image.shape[:2]
part_width = width // 3
average_brightness = []
for i in range(3):
    x_start = i * part_width
    x_end = (i + 1) * part_width if i < 2 else width
    part = original_image[:, x_start:x_end]
    brightness = np.mean(part)
    average_brightness.append(brightness)

print(f"Durchschnittliche Helligkeit der Teile: {average_brightness}")
contrast_value = model.predict(np.array([average_brightness]))[0]
image_contrast = m.enhance_contrast(original_image, contrast_value[0], 0)

# Kontrasterhöhung und Binärmaske
if len(image_contrast.shape) == 3 and image_contrast.shape[2] == 3:
    white_mask = np.all(image_contrast >= THRESHOLD, axis=-1)
    image_contrast[:] = [0, 0, 0]
    image_contrast[white_mask] = [1, 1, 1]
else:
    white_mask = image_contrast >= THRESHOLD
    image_contrast[:] = 0
    image_contrast[white_mask] = 1

# Größte zusammenhängende Komponente extrahieren
labels = measure.label(image_contrast, connectivity=2)
properties = measure.regionprops(labels)
if properties:
    largest_component = max(properties, key=lambda x: x.area)
    largest_label = largest_component.label
    largest_mask = labels == largest_label
    image_contrast = np.zeros_like(image_contrast)
    image_contrast[largest_mask] = 1
    centroid = largest_component.centroid

    # Delta_x berechnen
    image_center_x = width / 2
    centroid_x = centroid[1]
    delta_x = centroid_x - image_center_x
    print(f"Delta x: {delta_x}")

    # Visualisierung mit eingezeichneter Linie
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(image_contrast, cmap="gray")
    ax.axvline(image_center_x, color='blue', linestyle='--', label="Bildmitte")
    ax.scatter([centroid_x], [centroid[0]], color='red', label="Schwerpunkt")
    ax.plot([image_center_x, centroid_x], [centroid[0], centroid[0]], color='green', linewidth=2, label=r'$\Delta x$')
    ax.set_title(r"Visualisierung von $\Delta x$")
    plt.show()
