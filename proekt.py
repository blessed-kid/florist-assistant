from ultralytics import YOLO

def obuch():
    model = YOLO("yolo26s.pt")
    result = model.train(
        data="data.yaml",
        epochs = 10,
        imgsz = 640,
        batch = 16,
    )
    
    k= model.val()
    model.save('flowerassist/models/versionYOLO.pt')
    # test = model.val(test)
if __name__ == "__main__":
    obuch()

