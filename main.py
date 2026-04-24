from interface import ImageApp
import tkinterdnd2 as tkdnd
from assistant import Assistant
import cv2
from ultralytics import YOLO
model=YOLO("flowerassist/models/versionYOLO.pt")

def main():
    assistant2 = Assistant(path = "photo_flower.jpg")
    cap = cv2.imread(assistant2)
    success, frame = cap.read()
    if success:
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow('YOLO11 Detection', annotated_frame)
    # cap.release()
    
    root = tkdnd.Tk()
    app = ImageApp(root)
    root.mainloop()
    
if __name__=='__main__':
    main()