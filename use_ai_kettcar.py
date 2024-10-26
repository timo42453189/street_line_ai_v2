from TensorflowModelTest import TensorflowModelTest
from ImageDisplayer import ImageDisplayer
from ImageManipulator import ImageManipulator
import numpy as np
from skimage import measure
from camera.camera import Cam
import serial
import time
import cv2

ser = serial.Serial("/dev/ttyACM0", 115200)
time.sleep(3)

c = Cam(index=[0])
m = ImageManipulator()
model = TensorflowModelTest('contrast_model/v0_contrast.h5')
threshold = 0.9
Kp = 0.03

def calculate_angle(x):
    return -9*x+7

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
        #time.sleep(1)
        
    else:
        print("Keine weißen Bereiche im Bild gefunden.")
        steering_direction = 0
        ser.write(str(int(calculate_angle(0))).encode())