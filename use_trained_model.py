from TensorflowModelTest import TensorflowModelTest
from ImageDisplayer import ImageDisplayer
from data_storing.DataReader import DataReader
from ImageManipulator import ImageManipulator
import numpy as np
from skimage import measure
from camera.camera import Cam

c = Cam(index=[0])
d = DataReader()
m = ImageManipulator()
model = TensorflowModelTest('model_architectures/models/v0_contrast.h5')

image = c.resize_image(c.get_frame())
print(image.shape)
image = image / 255
original_image = image.copy()

height, width = original_image.shape[:2]
part_width = width // 3

average_brightness = []
for i in range(3):
    x_start = i * part_width
    x_end = (i + 1) * part_width if i < 2 else width
    part = original_image[:, x_start:x_end]
    brightness = np.mean(part)
    average_brightness.append(brightness)

print("Durchschnittliche Helligkeit der Bilddrittel:", average_brightness)
coordinates = model.predict(np.array([average_brightness]))[0]
print("Koordinaten aus dem Modell:", coordinates)

image_contrast = m.enhance_contrast(original_image, coordinates[0], 0)

# Definieren eines Schwellenwerts, um Pixel als weiß zu betrachten
threshold = 0.9

# Konvertieren des Bildes in ein binäres Bild (Schwarz-Weiß)
if len(image_contrast.shape) == 3 and image_contrast.shape[2] == 3:
    white_mask = np.all(image_contrast >= threshold, axis=-1)
    image_contrast[:] = [0, 0, 0]
    image_contrast[white_mask] = [1, 1, 1]
else:
    white_mask = image_contrast >= threshold
    image_contrast[:] = 0
    image_contrast[white_mask] = 1

# Labeln der verbundenen Komponenten im Bild
labels = measure.label(image_contrast, connectivity=2)

# Berechnen der Eigenschaften jeder verbundenen Komponente
properties = measure.regionprops(labels)

if properties:
    # Finden der Komponente mit der größten Fläche
    largest_component = max(properties, key=lambda x: x.area)
    largest_label = largest_component.label

    # Erstellen einer Maske, die nur die größte Komponente enthält
    largest_mask = labels == largest_label

    # Aktualisieren des Bildes, um nur die größte Komponente zu behalten
    image_contrast = np.zeros_like(image_contrast)
    image_contrast[largest_mask] = 1

    # Berechnen des Schwerpunkts der größten Komponente
    centroid = largest_component.centroid  # (Zeile, Spalte)
    print("Schwerpunkt der größten Komponente:", centroid)

    # Berechnen der Differenz zwischen Schwerpunkt und Bildmitte
    image_center_x = width / 2
    centroid_x = centroid[1]
    delta_x = centroid_x - image_center_x

    # Einfache Proportionalregelung für die Lenkung
    Kp = 0.01  # Lenkempfindlichkeit
    steering_direction = Kp * delta_x

    if steering_direction > 0:
        direction = "rechts"
    elif steering_direction < 0:
        direction = "links"
    else:
        direction = "geradeaus"

    print(f"Lenke {direction} (Lenkwinkel: {steering_direction:.2f})")
else:
    print("Keine weißen Bereiche im Bild gefunden.")
    steering_direction = 0  # Standardmäßig geradeaus fahren

# Anzeigen des resultierenden Bildes
displayer = ImageDisplayer(image)
displayer.display()

displayer = ImageDisplayer(image_contrast)
displayer.display()
