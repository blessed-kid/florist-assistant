from interface import ImageApp
import tkinterdnd2 as tkdnd
from assistant import Assistant
import cv2
from ultralytics import YOLO
model=YOLO("C:/Users/admin/Documents/runs/detect/train36/weights/best.pt")

def main():
    path = "photo_flower.jpg"
    # assistant2 = Assistant(path = str)
    results = model.predict(source = "C:/Users/admin/Documents/florist-assistant/folder_with_photos", conf = 0.1)
    # result[0].show()
    for result in results:
        result.show()
    
    # root = tkdnd.Tk()
    # app = ImageApp(root)
    # root.mainloop()
    
if __name__=='__main__':
    main()