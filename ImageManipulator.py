import cv2

class ImageManipulator:
    def gaussian_blur(self, image):
        return cv2.GaussianBlur(image, (5,5), 0)
    
    def enhance_contrast(self,image, contrast, brightness):
        import numpy as np
        return cv2.addWeighted(image, contrast, np.zeros(image.shape, image.dtype), 0, brightness) 

    def colormap(self, image):
        return cv2.applyColorMap(image, cv2.COLORMAP_HOT)
    
    def threshold(self, image, threshold):
        import numpy as np
        mask = np.all(image > threshold, axis=-1)
        image = np.zeros_like(image)
        image[mask] = [255, 255, 255]
        return image

    def calculate_average_light(self, image):
        return (image[0].sum() + image[1].sum() + image[2].sum()) / (image.shape[0] * image.shape[1])

    def convert_to_gray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)