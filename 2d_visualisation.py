from TensorflowModelTest import TensorflowModelTest
from ImageDisplayer import ImageDisplayer
from ImageManipulator import ImageManipulator
import numpy as np
from skimage import measure
from camera.camera import Cam
#import serial
import time
import cv2
import os

# Initialize the serial port
#ser = serial.Serial("COM9", 115200)
time.sleep(3)

CONTRAST_FILE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'files', 'contrast_value.txt')
AI_FIRST_IMAGE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'images', 'ai_first_image.jpg')
AI_SECOND_IMAGE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'images', 'ai_second_image.jpg')
AI_THIRD_IMAGE_PATH = os.path.join(os.getcwd(), 'webserver', 'static', 'images', 'ai_third_image.jpg')
# Load the Camera, Image Manipulator and Model
c = Cam(index=[0])
m = ImageManipulator()
model = TensorflowModelTest('contrast_model/v0_contrast.h5')

# Constants
THRESHOLD = 0.9
KP = 0.03


def calculate_angle(x):
    """
    Calculates the corresponding steering angle for the Arduino.
    
    Parameters
    ----------
    x : float
        The input value.

    Returns
    -------
    float
        The calculated steering angle.
    """
    return 495*x+510

def draw_bezier_curve(image ,p0 ,p1 ,p2 ,curvature_factor=1.0 ,color=(0, 255, 0) , thickness=2):
    """
    ################ THIS FUNCTION WAS GENERATED BY CHATGPT ################
    Draws a Bezier curve on a given image using 3 points

    Parameters
    ----------
    image : numpy.ndarray
        The image to draw the curve on.
    p0 : tuple
        Start point of the bezier curve.
    p1 : tuple
        Middle point of the bezier curve.
    p2 : tuple
        End point of the bezier curve.
    curvature_factor : float, optional
        Controls the curvature of the curve. Default is 1.0.
    color : tuple, optional
        Color of the curve. Default is (0, 255, 0).
    thickness : int, optional
        Thickness of the curve. Default is 2.
    
    Returns
    -------
    numpy.ndarray
        The image with the curve drawn on it.
    """
    image = cv2.rectangle(image, (140, 70), (190, 80), color=(255, 0, 0), thickness=-1)
    p1 = np.array(p0) + curvature_factor * (np.array(p1) - np.array(p0))
    def bezier_curve(p0, p1, p2, t):
        return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
    curve_points = []
    for t in np.linspace(0, 1, 100):
        point = bezier_curve(np.array(p0), np.array(p1), np.array(p2), t)
        curve_points.append(point.astype(int))

    for i in range(len(curve_points) - 1):
        cv2.line(image, tuple(curve_points[i]), tuple(curve_points[i + 1]), color, thickness)
    return image

send_image = 0
TRESHOLD_IMAGE_SEND = 20
while True:
    # Takes an image from the webcam and resize it
    image = c.resize_image(c.get_frame())
    # Save image to folder for Server visualization
    if send_image > TRESHOLD_IMAGE_SEND:
        cv2.imwrite(AI_FIRST_IMAGE_PATH, image)
    # Normalize the image for the AI
    image = image / 255
    # Make a copy of the original image for the visualisation
    original_image = image.copy()

    # Divide the image in 3 parts
    height, width = original_image.shape[:2]
    part_width = width // 3

    # Calculate the average brightness of every part
    # average_brightness: List[float] --> Input for the AI model
    average_brightness = []
    for i in range(3):
        x_start = i * part_width
        x_end = (i + 1) * part_width if i < 2 else width
        part = original_image[:, x_start:x_end]
        brightness = np.mean(part)
        average_brightness.append(brightness)

    # Predict the contrast of the image
    contrast_value = model.predict(np.array([average_brightness]))[0]
    # Write contrast value to file for Server visualization
    if send_image > TRESHOLD_IMAGE_SEND:
        with open(CONTRAST_FILE_PATH, 'w') as file:
            file.write(str(contrast_value[0]))
    # Enhance the contrast of the image corresponding to the predicted value
    image_contrast = m.enhance_contrast(original_image, contrast_value[0], 0)
    # Generate a mask making the white parts white and the rest black to get a heatmap of the street
    if len(image_contrast.shape) == 3 and image_contrast.shape[2] == 3:
        white_mask = np.all(image_contrast >= THRESHOLD, axis=-1)
        image_contrast[:] = [0, 0, 0]
        image_contrast[white_mask] = [1, 1, 1]
    else:
        white_mask = image_contrast >= THRESHOLD
        image_contrast[:] = 0
        image_contrast[white_mask] = 1

    # Save image_contrast to folder for Server visualization
    if send_image > TRESHOLD_IMAGE_SEND:
        cv2.imwrite(AI_SECOND_IMAGE_PATH, image_contrast*255)
    
    # Extract all white componets of the image
    labels = measure.label(image_contrast, connectivity=2)
    properties = measure.regionprops(labels)

    if properties:
        # Find the component with the largest area and extract it
        largest_component = max(properties, key=lambda x: x.area)
        largest_label = largest_component.label
        largest_mask = labels == largest_label
        image_contrast = np.zeros_like(image_contrast)
        image_contrast[largest_mask] = 1
        # Save image_contrast to folder for Server visualization
        if send_image > TRESHOLD_IMAGE_SEND:
            cv2.imwrite(AI_THIRD_IMAGE_PATH, image_contrast*255)
        # Find the centroid of the largest component
        centroid = largest_component.centroid
        print("Schwerpunkt der größten Komponente:", centroid)
        # Calculate the delta_x between the centroid and the image center
        image_center_x = width / 2
        centroid_x = centroid[1]
        delta_x = centroid_x - image_center_x
        # Multiply the delta_x with the KP constant to get correspoinding steering angle
        steering_direction = KP * delta_x

        print(f"(Steering angle: {steering_direction:.2f})")
        print(f"Steering angle for Arduino: {calculate_angle(steering_direction)}")
        # Send the calculated steering angle to the Arduino
        #ser.write(str(int(calculate_angle(steering_direction))).encode())
        # Calculate the parameters for visualization and draw the bezier curve
        p0 = (140, 70)
        p1 = (140, 50)
        p2 = (140*(steering_direction+1), 20)
        image_contrast = draw_bezier_curve(image_contrast, p0, p1, p2)
        p0 = (190, 70)
        p1 = (190, 50)
        p2 = (190*(steering_direction+1), 20)
        image_contrast = draw_bezier_curve(image_contrast, p0, p1, p2)
        # Display the image for visualisation
        cv2.imshow('road', image_contrast)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        #time.sleep(1)
        
    else:
        print("No white area found.")
        steering_direction = 0
        #ser.write(str(int(calculate_angle(0))).encode())
    send_image +=1
    if send_image==TRESHOLD_IMAGE_SEND+2:
        print("RESET")
        send_image = 0