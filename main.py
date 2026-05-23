from new_interface import App_for_assistant
import tkinterdnd2 as tkdnd
from assistant import Assistant
import cv2
from ultralytics import YOLO
# model=YOLO("C:/Users/admin/Documents/runs/detect/train36/weights/best.pt")

def main():
    root = tkdnd.Tk()
    app = App_for_assistant(root)
    root.mainloop()
    
if __name__=='__main__':
    main()