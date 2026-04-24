import numpy as np
import cv2

class Assistant:
    def __init__(self, path:str):
        image = cv2.imread(path)
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    def processing_picture(self, image):
        image = cv2.medianBlur(image,5)
        kernel = np.ones((5,5),np.uint8)
        image = cv2.dilate(image, kernel, iterations = 1)
        image = cv2.erode(image, kernel, iterations = 1)
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        return image