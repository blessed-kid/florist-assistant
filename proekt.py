from ultralytics import YOLO

def obuch():
    model = YOLO("C:/Users/admin/Documents/runs/detect/train36/weights/best.pt")
    result = model.train(
        data="C:/Users/admin/Documents/florist-assistant/flowers_yolo26/data.yaml",
        epochs = 20,
        imgsz = 640,
        batch = 64,
    )
    
    k= model.val()
    # test = "C:/Users/admin/Documents/florist-assistant/flowers_yolo26/test/images"
    # test = model.(test)
    # test = model.val(test)
    # result = model.predict(model='florist-assistant/yolo26n.pt', source="C:/Users/admin/Documents/florist-assistant/flowers_yolo26/test/images")
    metrics = model.val(data="C:/Users/admin/Documents/florist-assistant/flowers_yolo26/data.yaml", split = 'test')
    model.save('florist-assistant/yolo26n.pt')
    result = model.predict(source = "C:/Users/admin/Documents/florist-assistant/flowers_yolo26/test/images", save = True, conf = 0.1)
    
if __name__ == "__main__":
    obuch()

