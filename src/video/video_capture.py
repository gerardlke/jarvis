import cv2

class VideoCapture:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_name = "Camera"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (self.frame_width, self.frame_height))

    def read(self):
        return self.cam.read()
    
    def show(self, frame):
        cv2.imshow(self.frame_name, cv2.flip(frame, 1))

    def write(self, frame):
        self.out.write(frame)
    
    def plot_rectangle(self, frame, xyxy):
        cv2.rectangle(frame, [int(num) for num in xyxy[:2]], [int(num) for num in xyxy[2:]], (255, 0, 0), 2)
    
    def plot_keypoints(self, frame, keypoints):
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),           # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),           # Index
            (0, 9), (9, 10), (10, 11), (11, 12),      # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),    # Ring
            (0, 17), (17, 18), (18, 19), (19, 20)     # Pinky
        ]
        
        for start, end in connections:
                pt1 = tuple(map(int, keypoints[start]))
                pt2 = tuple(map(int, keypoints[end]))
                cv2.line(frame, pt1, pt2, (255, 255, 255), 2)

        # Draw Points on top
        for kp in keypoints:
            cv2.circle(frame, (int(kp[0]), int(kp[1])), 4, (0, 0, 255), -1)

    def process_gesture(self, results):
        return

    def stop(self):
        key_pressed = cv2.waitKey(1) & 0xFF == ord("q")
        window_closed = cv2.getWindowProperty(self.frame_name, cv2.WND_PROP_VISIBLE) < 1
        return key_pressed or window_closed

    def shutdown(self):
        self.cam.release()
        self.out.release()
        cv2.destroyAllWindows()

    