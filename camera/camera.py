import cv2

class Cam:
    def __init__(self, index=[0]):
        self.cams = []
        for i in range(len(index)):
            x = cv2.VideoCapture(index[i], cv2.CAP_DSHOW)#cv2.CAP_DSHOW
            if x.isOpened():
                self.cams.append(x)
            else:
                raise Exception("Camera port", index[i], "is not available")

    def getAvailableCameras(self):
        return self.cams

    def get_frame(self, camera_index=0):
        ret, frame = self.cams[camera_index].read()
        if ret:
            return frame

    def show_image(self, frame):
        cv2.imshow('frame', frame)
        cv2.waitKey(0)

    def scale_down(self, frame):
        return cv2.resize(frame, (0, 0), fx=0.4, fy=0.3)

    def image_canny(self, frame):
        return cv2.Canny(frame, 100, 200)

    def remove_color_dimension(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def resize_image(self, frame):
        return cv2.resize(frame, (320,80), interpolation = cv2.INTER_AREA)

    def prepare_image(self, frame):
        frame = self.remove_color_dimension(frame)
        frame = cv2.resize(frame, (250, 170), interpolation = cv2.INTER_AREA)
        frame = self.image_canny(frame)
        return frame

    # define a function to combine the lists of 2 images to one big list
    def combine_images(self, img1, img2):
        return cv2.hconcat([img1, img2])