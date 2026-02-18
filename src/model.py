from ultralytics import YOLO

class Model:
    def __init__(self, model):
        self.model = YOLO(model)

    def predict(self, src):
        return self.model(src)
    
    def extract_bbox(self, result):
        return result.boxes.xyxy[0].cpu().numpy()