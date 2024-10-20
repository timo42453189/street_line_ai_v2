import cv2

class ImageDisplayer:
    def __init__(self, image, lines=None):
        self.image = image
        self.lines = lines
    def display(self):
        if self.lines is not None:
            self.image = cv2.convertScaleAbs(self.image)
            try:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            except:
                pass
            pt1_line1 = tuple(map(int, self.lines[0][0]))
            pt2_line1 = tuple(map(int, self.lines[0][1]))
            pt1_line2 = tuple(map(int, self.lines[1][0]))
            pt2_line2 = tuple(map(int, self.lines[1][1]))
            self.image = cv2.line(self.image, pt1_line1, pt2_line1, (0,0,255), 3)
            self.image = cv2.line(self.image, pt1_line2, pt2_line2, (0,0,255), 3)
        cv2.imshow('image', self.image)
        cv2.waitKey(0)