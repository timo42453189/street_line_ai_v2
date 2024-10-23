from TensorflowModelTest import TensorflowModelTest
from ImageDisplayer import ImageDisplayer
from data_storing.DataReader import DataReader
from ImageManipulator import ImageManipulator
import numpy as np
from skimage import measure
from camera.camera import Cam
import cv2

d = DataReader()
m = ImageManipulator()
model = TensorflowModelTest('contrast_model/v0_contrast.h5')

image, _ = d.read("400.h5", "train_images")
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

threshold = 0.9

if len(image_contrast.shape) == 3 and image_contrast.shape[2] == 3:
    white_mask = np.all(image_contrast >= threshold, axis=-1)
    image_contrast[:] = [0, 0, 0]
    image_contrast[white_mask] = [1, 1, 1]
else:
    white_mask = image_contrast >= threshold
    image_contrast[:] = 0
    image_contrast[white_mask] = 1

labels = measure.label(image_contrast, connectivity=2)

properties = measure.regionprops(labels)

if properties:
    largest_component = max(properties, key=lambda x: x.area)
    largest_label = largest_component.label

    largest_mask = labels == largest_label

    image_contrast = np.zeros_like(image_contrast)
    image_contrast[largest_mask] = 1

    centroid = largest_component.centroid  # (Zeile, Spalte)
    print("Schwerpunkt der größten Komponente:", centroid)

    image_center_x = width / 2
    centroid_x = centroid[1]
    delta_x = centroid_x - image_center_x

    Kp = 0.01
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
    steering_direction = 0


def draw_bezier_curve(image, p0, p1, p2, curvature_factor=1.0, color=(0, 255, 0), thickness=2):
    # Generiert von ChatGPT
    p1 = np.array(p0) + curvature_factor * (np.array(p1) - np.array(p0))
    def bezier_curve(p0, p1, p2, t):
        return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
    curve_points = []
    for t in np.linspace(0, 1, 100):  # 100 Punkte auf der Kurve
        point = bezier_curve(np.array(p0), np.array(p1), np.array(p2), t)
        curve_points.append(point.astype(int))

    for i in range(len(curve_points) - 1):
        cv2.line(image, tuple(curve_points[i]), tuple(curve_points[i + 1]), color, thickness)

    #cv2.circle(image, tuple(p0), 5, (0, 255, 0), -1)
    #cv2.circle(image, tuple(p1.astype(int)), 5, (255, 0, 0), -1)
    #cv2.circle(image, tuple(p2), 5, (0, 255, 0), -1)
    return image


image_contrast = cv2.rectangle(image_contrast, (140, 70), (190, 80), color=(255, 0, 0), thickness=-1)
print(image_contrast.shape)
p0 = (140, 70)   # Startpunkt (A)
p1 = (140, 50)  # Kontrollpunkt (C)
p2 = (140*(steering_direction+1), 20)  # Endpunkt (B)
image_contrast = draw_bezier_curve(image_contrast, p0, p1, p2)
p0 = (190, 70)   # Startpunkt (A)
p1 = (190, 50)  # Kontrollpunkt (C)
p2 = (190*(steering_direction+1), 20)  # Endpunkt (B)
image_contrast = draw_bezier_curve(image_contrast, p0, p1, p2)
cv2.imshow('road', image_contrast)
cv2.waitKey(0)