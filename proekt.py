from ultralytics import YOLO
import matplotlib
import numpy as np
import cv2
import pymorphy2
from interface import ImageApp
import tkinterdnd2 as tkdnd

def main():
    model = YOLO("yolo26s.pt")
    result = model.train(
        data="data.yaml",
        epochs = 10,
        imgsz = 640,
        batch = 16,
    )
    
    k= model.val()
    # test = model.val(test)
if __name__ == "__main__":
    main()

