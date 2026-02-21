import asyncio

from .video.cv_model import CVModel
from .video.gesture import Gesture
from .video.video_capture import VideoCapture

from .audio.sr_model import SRModel
from .audio.audio_capture import AudioCapture
from .audio.audio_detector import AudioDetector
from .audio.speech_buffer import SpeechBuffer

from .event_manager import EventManager

class Pipeline:
    def __init__(self):
        print("Initialising pipeline...")
        # Start video capture tools
        self.vid = VideoCapture()
        self.cv_model = CVModel(r"models\runs\pose\hand-keypoints\weights\best.pt")
        self.gesture = Gesture(r"models\runs\knn\knn.joblib", r"models\runs\knn\scaler.joblib")

        # Start audio capture tools
        self.audio_capture = AudioCapture()
        self.audio_detector = AudioDetector()
        self.speech_buffer = SpeechBuffer()
        self.sr_model = SRModel("small.en")

        # Start event manager
        self.events = EventManager()

        self.running = True
        print("Pipeline started.")

    async def video_loop(self):
        while self.running:
            frame = await asyncio.to_thread(self.vid.read)

            # Video detections
            results = self.cv_model.predict(frame)

            # Using keypoints to detect gesture
            _, keypoints = self.process_video(frame, results)
            confidence, gesture = self.gesture.detect_gesture(keypoints)
            if gesture:
                await self.events.update_gesture(gesture)

            # Update window based on states
            state = await self.events.get_state()
            self.vid.overlay_text(frame, state.mode, (50, 50))
            if state.last_command:
                self.vid.overlay_text(frame, state.last_command, (50, 100))
            if state.last_gesture:
                self.vid.overlay_text(frame, state.last_gesture, (50, 150))

            # Display window
            self.vid.show(frame)
            await asyncio.to_thread(self.vid.show, frame)

            if self.vid.stop():
                self.running = False

            await asyncio.sleep(0)
    
    def process_video(self, frame, results):
        # Extracts bbox and keypoints from results (but currently only takes last)
        for result in results:
            box = self.cv_model.extract_bbox(result)
            if len(box) > 0:
                self.vid.plot_rectangle(frame, box)

            keypoints = self.cv_model.extract_keypoints(result)
            if len(keypoints) > 0:
                self.vid.plot_keypoints(frame, keypoints)

        return box, keypoints
    
    async def audio_loop(self):
        while self.running:
            audio = await asyncio.to_thread(self.audio_capture.read)

            # If noise level crosses threshold, considered speaking
            speaking = self.audio_detector.update(audio)

            # Accumulate enough frames in buffer while speaking
            if speaking:
                self.speech_buffer.add(audio)
            # Send for speech recognition if buffer is full or user stops speaking
            elif (not speaking and self.speech_buffer.buffer) or (speaking and not self.speech_buffer.too_short()):
                speech = self.speech_buffer.get_audio()
                self.speech_buffer.reset()
                text = await asyncio.to_thread(self.sr_model.transcribe, speech)
                await self.events.update_command(text)
            
            await asyncio.sleep(0)

    async def run(self):
        await asyncio.gather(
            self.video_loop(),
            self.audio_loop()
        )