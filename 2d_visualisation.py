from TensorflowModelTest import TensorflowModelTest
from ImageDisplayer import ImageDisplayer
from ImageManipulator import ImageManipulator
import numpy as np
from skimage import measure
from camera.camera import Cam
import serial
import time
import cv2

ser = serial.Serial("COM9", 115200)
time.sleep(3)

c = Cam(index=[1])
m = ImageManipulator()
model = TensorflowModelTest('contrast_model/v0_contrast.h5')
threshold = 0.9
Kp = 0.03

def calculate_angle(x):
    return -9*x+7

def draw_bezier_curve(image ,p0 ,p1 ,p2p ,curvature_factor=1.0 ,color=(0, 255, 0) , thickness=2):
    # Generiert von ChatGPT
    image = cv2.rectangle(image, (140, 70), (190, 80), color=(255, 0, 0), thickness=-1)
    p1 = np.array(p0) + curvature_factor * (np.array(p1) - np.array(p0))
    def bezier_curve(p0, p1, p2, t):
        return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
    curve_points = []
    for t in np.linspace(0, 1, 100):  # 100 Punkte auf der Kurve
        point = bezier_curve(np.array(p0), np.array(p1), np.array(p2), t)
        curve_points.append(point.astype(int))

    for i in range(len(curve_points) - 1):
        cv2.line(image, tuple(curve_points[i]), tuple(curve_points[i + 1]), color, thickness)
    return image


while True:
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

    coordinates = model.predict(np.array([average_brightness]))[0]
    image_contrast = m.enhance_contrast(original_image, coordinates[0], 0)
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
        steering_direction = Kp * delta_x

        print(f"(Lenkwinkel: {steering_direction:.2f})")
        print(f"Neuer Lenkwinkel: {calculate_angle(steering_direction)}")
        ser.write(str(int(calculate_angle(steering_direction))).encode())
        p0 = (140, 70)
        p1 = (140, 50)
        p2 = (140*(steering_direction+1), 20)
        image_contrast = draw_bezier_curve(image_contrast, p0, p1, p2)
        p0 = (190, 70)
        p1 = (190, 50)
        p2 = (190*(steering_direction+1), 20)
        image_contrast = draw_bezier_curve(image_contrast, p0, p1, p2)
        cv2.imshow('road', image_contrast)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        #time.sleep(1)
        
    else:
        print("Keine weißen Bereiche im Bild gefunden.")
        steering_direction = 0
        ser.write(str(int(calculate_angle(0))).encode())