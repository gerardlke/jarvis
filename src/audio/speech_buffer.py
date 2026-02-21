import numpy as np

RATE = 16000

class SpeechBuffer:
    def __init__(self):
        self.buffer = []

    def add(self, frame):
        self.buffer.append(frame)

    def too_short(self):
        return len(self.buffer) < RATE

    def reset(self):
        self.buffer = []

    def get_audio(self):
        audio_bytes = b"".join(self.buffer)
        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
        return audio_int16.astype(np.float32) / 32768.0