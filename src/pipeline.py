from .model import Model
from .video_capture import VideoCapture

class Pipeline:
    def __init__(self):
        self.vid = VideoCapture()
        self.model = Model(r"models\yolo26s-pose.pt")

    def main(self):
        while True:
            ret, frame = self.vid.read()

            results = self.model.predict(frame)
            for result in results:
                xyxy = self.model.extract_bbox(result)
                self.vid.plot_rectangle(frame, xyxy)
            self.vid.show(frame)

            if self.vid.stop():
                break

        # Release the capture and writer objects
        self.vid.shutdown()