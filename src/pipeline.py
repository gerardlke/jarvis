import asyncio

from .video.display import Display
from .video.gesture import Gesture
from .video.cv_model import CVModel
from .video.video_capture import VideoCapture

from .audio.sr_model import SRModel
from .audio.audio_capture import AudioCapture
from .audio.audio_detector import AudioDetector
from .audio.speech_buffer import SpeechBuffer

from .brain.schemas.logger import Logger
from .brain.controller import Controller

from .event_manager import EventManager


class Pipeline:
    Logger.setup()

    def __init__(self):
        Logger.info("Pipeline", "Initialising pipeline...")
        # Start video capture tools
        self.vid = VideoCapture()
        self.display = Display(self.vid.frame_width, self.vid.frame_height)
        self.cv_model = CVModel(r"models\runs\pose\hand-keypoints\weights\best.pt")
        self.gesture = Gesture(r"models\runs\knn\knn.joblib", r"models\runs\knn\scaler.joblib")

        # Start audio capture tools
        self.audio_capture = AudioCapture()
        self.audio_detector = AudioDetector()
        self.speech_buffer = SpeechBuffer()
        self.sr_model = SRModel("small.en")

        # Start main controllers
        self.events = EventManager()
        self.controller = Controller()

        self.running = True
        Logger.info("Pipeline", "Pipeline started.")


    async def video_loop(self):
        Logger.info("Pipeline", "Video loop started.")
        while self.running:
            frame = await asyncio.to_thread(self.vid.read)

            # Video detections
            results = self.cv_model.predict(frame)

            # Using keypoints to detect gesture
            processed_results = self.cv_model.process_results(results)
            keypoints = [result.get("keypoints", None) for result in processed_results]
            confidence, gesture = self.gesture.detect_gesture(keypoints[0])
            await self.events.update_gesture(gesture if gesture else None, confidence if gesture else 0.0)

            # Update window based on states
            state = await self.events.get_state()
            frame = self.display.render(frame, state, processed_results)
            
            # Display window
            self.vid.show(frame)
            await asyncio.to_thread(self.vid.show, frame)

            if self.vid.stop():
                self.running = False

            await asyncio.sleep(0)
    

    async def audio_loop(self):
        Logger.info("Pipeline", "Audio loop started.")
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

    async def action_loop(self):
        Logger.info("Pipeline", "Action loop started.")
        while self.running:
            state = await self.events.get_state()
            command, gesture = state.last_command, state.last_gesture

            response = await asyncio.to_thread(self.controller.run, (command, gesture))

            await self.events.update_response(response)

            await asyncio.sleep(0)

    async def run(self):
        await asyncio.gather(
            self.video_loop(),
            self.audio_loop(),
            self.action_loop()
        )