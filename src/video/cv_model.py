from ultralytics import YOLO

class CVModel:
    def __init__(self, model):
        self.model = YOLO(model)

    def predict(self, src):
        return self.model(src, verbose=False)
    
    def extract_bbox(self, result):
        if len(result.boxes.xyxy) == 0:
            return ()
        return result.boxes.xyxy[0].cpu().numpy()

    def extract_keypoints(self, result):
        if len(result.keypoints.xy) == 0:
            return ()
        return result.keypoints.xy[0].cpu().numpy()