import cv2

class VideoCapture:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_name = "Camera"

    def read(self):
        ret, frame = self.cam.read()
        frame = cv2.flip(frame, 1)
        return frame
    
    def show(self, frame):
        cv2.imshow(self.frame_name, frame)

    def write(self, frame):
        self.out.write(frame)

    def stop(self):
        key_pressed = cv2.waitKey(1) & 0xFF == ord("q")
        window_closed = cv2.getWindowProperty(self.frame_name, cv2.WND_PROP_VISIBLE) < 1
        return key_pressed or window_closed

    def shutdown(self):
        self.cam.release()
        self.out.release()
        cv2.destroyAllWindows()

    