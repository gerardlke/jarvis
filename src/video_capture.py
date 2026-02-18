import cv2

class VideoCapture:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (self.frame_width, self.frame_height))

    def read(self):
        return self.cam.read()
    
    def show(self, frame):
        cv2.imshow("Camera", frame)

    def write(self, frame):
        self.out.write(frame)

    def stop(self):
        key_pressed = cv2.waitKey(1) & 0xFF == ord("q")
        window_closed = cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1
        return key_pressed or window_closed

    def shutdown(self):
        self.cam.release()
        self.out.release()
        cv2.destroyAllWindows()
    
    def plot_rectangle(self, frame, xyxy):
        cv2.rectangle(frame, [int(num) for num in xyxy[:2]], [int(num) for num in xyxy[2:]], (255, 0, 0), 2)

    