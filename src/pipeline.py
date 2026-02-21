import asyncio

from .video.cv_model import CVModel
from .video.video_capture import VideoCapture

from .audio.sr_model import SRModel
from .audio.audio_capture import AudioCapture
from .audio.audio_detector import AudioDetector
from .audio.speech_buffer import SpeechBuffer

class Pipeline:
    def __init__(self):
        self.vid = VideoCapture()
        self.cv_model = CVModel(r"models\runs\pose\hand-keypoints\weights\best.pt")

        self.audio_capture = AudioCapture()
        self.audio_detector = AudioDetector()
        self.speech_buffer = SpeechBuffer()
        self.sr_model = SRModel("small.en")

        self.running = True

    async def video_loop(self):
        while self.running:
            ret, frame = await asyncio.to_thread(self.vid.read)

            # Video detections
            results = self.cv_model.predict(frame)

            self.process_video(frame, results)
            gesture = self.vid.process_gesture(results)
            if gesture:
                pass

            self.vid.show(frame)

            await asyncio.to_thread(self.vid.show, frame)

            if self.vid.stop():
                self.running = False

            await asyncio.sleep(0)
    
    def process_video(self, frame, results):
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
            frame = await asyncio.to_thread(self.audio_capture.read)

            speaking = self.audio_detector.update(frame)

            if speaking:
                self.speech_buffer.add(frame)
            elif (not speaking and self.speech_buffer.buffer) or (speaking and not self.speech_buffer.too_short()):
                audio = self.speech_buffer.get_audio()
                self.speech_buffer.reset()

                text = await asyncio.to_thread(self.sr_model.transcribe, audio)
                print("Recognized:", text)
            
            await asyncio.sleep(0)

    async def run(self):
        await asyncio.gather(
            self.video_loop(),
            self.audio_loop()
        )