from data_storing.DataReader import DataReader
from ImageDisplayer import ImageDisplayer
from ImageManipulator import ImageManipulator
import numpy as np
import cv2
import os

m = ImageManipulator()
d = DataReader()

for x in os.listdir("data_storing/train_images"):
    image, _ = d.read(x, 'train_images')
    image = image / 255.0
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

    print(f"Durchschnittliche Helligkeit der Teile: {average_brightness}")

    contrast_value = 1.5

    while True:
        image_adjusted = m.enhance_contrast(original_image, contrast_value, 0)

        cv2.imshow('Adjust Contrast', image_adjusted)

        key = cv2.waitKey(0) & 0xFF

        if key == 27:
            break
        elif key == ord('s'):
            d.store_automatic(average_brightness, contrast_value, 'train_images_contrast')
            break
        elif key == ord('+') or key == ord('='):  # '+'-Taste zum Erhöhen des Kontrasts
            contrast_value += 0.1
            print(f"Kontrast erhöht auf {contrast_value:.1f}")
        elif key == ord('-') or key == ord('_'):  # '-'-Taste zum Verringern des Kontrasts
            contrast_value = max(0.1, contrast_value - 0.1)  # Verhindern, dass der Kontrast negativ wird
            print(f"Kontrast verringert auf {contrast_value:.1f}")
        else:
            print("Drücken Sie '+/-' um den Kontrast anzupassen, 's' zum Speichern oder ESC zum Überspringen.")
            continue

    # Fenster schließen bevor zum nächsten Bild gewechselt wird
    cv2.destroyAllWindows()
