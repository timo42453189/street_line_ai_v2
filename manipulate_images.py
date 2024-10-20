from data_storing.DataReader import DataReader
from ImageDisplayer import ImageDisplayer
from ImageManipulator import ImageManipulator
import os
def contrast_calculations(x):
    return (1.05**(-x+2))+1.5

reader = DataReader()
for image_name in os.listdir("data_storing/train_images"):
    print(image_name)
    image, coordinates = reader.read(f"{image_name}", 'train_images')
    manipulator = ImageManipulator()
    image = manipulator.gaussian_blur(image)
    brightness = manipulator.calculate_average_light(image)
    y = contrast_calculations(brightness)
    print(y, brightness)
    image = manipulator.enhance_contrast(image, y, 0)
    image = manipulator.colormap(image)
    image = manipulator.threshold(image, 235)
    image = manipulator.convert_to_gray(image)
    reader.store_automatic(image/255, coordinates/1000, 'train_images_enhanced')
    # displayer = ImageDisplayer(image)
    # displayer.display()