import cv2
import time
import numpy as np

class Display:
    PRIMARY_COLOR = (0, 255, 255)
    SECONDARY_COLOR = (80, 200, 200)
    TEXT_COLOR = (220, 220, 220)
    FONT = cv2.FONT_HERSHEY_SIMPLEX

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start_time = time.time()

        self.plot_bboxes = False
        self.plot_keypoints = True
    
    def render(self, frame, state, results=[]):
        # Plot bbox and keypoints
        for result in results:
            bbox = result.get("bbox", None)
            keypoints = result.get("keypoints", None)
            if self.plot_bboxes and len(bbox) > 0:
                Display.plot_rectangle(frame, bbox)
            if self.plot_keypoints and len(keypoints) > 0:
                Display.draw_keypoints(frame, keypoints)

        # Draw UI elements
        overlay = frame.copy()
        self.draw_top_bar(overlay, state)
        self.draw_transcript(overlay, state)
        return overlay

    # UI components

    def draw_top_bar(self, frame, state):
        x, y = 30, 30
        Display.overlay_text(frame, f"Mode: {state.mode}", (x, y), scale=0.7)

        if state.last_gesture:
            Display.overlay_text(frame, f"Gesture: {state.last_gesture}", (x, y * 2), scale=0.7)

            # Draw outer bar
            y = int(y * 2.5)
            max_width = 200
            max_height = 20
            Display.plot_rectangle(frame, (x, y, x + max_width, y + max_height))

            conf = state.gesture_conf
            if conf and conf > 0:
                # Only draw inner bar if valid confidence level
                bar_width = int(conf * max_width)
                Display.plot_rectangle(frame, (x, y, x + bar_width, y + max_height), thickness=-1)
                Display.overlay_text(frame, f"{int(conf * 100)}%", (x, y + max_height), scale=0.5)
    
    def draw_transcript(self, frame, state):
        if state.last_command:
            text = f'"{state.last_command}"'
            text_size = cv2.getTextSize(text, Display.FONT, 0.8, 2)[0]
            Display.overlay_text(frame, text, ((self.width - text_size[0]) // 2, self.height - 40), scale=0.8)

    def draw_keypoints(frame, keypoints):
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
                Display.plot_line(frame, pt1, pt2)

        for point in keypoints:
            Display.plot_circle(frame=frame, xy=(int(point[0]), int(point[1])))

    # Helper functions

    def plot_rectangle(frame, xyxy, thickness=1):
        cv2.rectangle(
            frame,
            [int(num) for num in xyxy[:2]],
            [int(num) for num in xyxy[2:]],
            Display.PRIMARY_COLOR,
            thickness
        )
    
    def plot_circle(frame, xy, radius=3):
        radius += int(radius * np.sin(time.time() * radius))
        cv2.circle(
            frame,
            xy,
            radius,
            Display.PRIMARY_COLOR,
            2
        )

    def plot_line(frame, xy1, xy2, width=1):
        cv2.line(
            frame,
            xy1,
            xy2,
            Display.SECONDARY_COLOR,
            width
        )
    
    def overlay_text(frame, text, location=(0, 0), scale=1):
        cv2.putText(
            frame,
            text,
            location,
            Display.FONT,
            scale,
            Display.TEXT_COLOR, 
            1, 
            cv2.LINE_AA
        )