from ultralytics import YOLO

def obuch():
    model = YOLO("yolo26n.pt")
    result = model.train(
        data="C:/Users/a.m.vershinin/Documents/flowerassist/flowers_yolo26/data.yaml",
        epochs = 50,
        imgsz = 640,
        batch = 16,
        val = False,
    )
    
    # k= model.val()
    model.save('flowerassist/yolo26n.pt')
    # test = model.val(test)
if __name__ == "__main__":
    obuch()

