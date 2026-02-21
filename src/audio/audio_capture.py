import pyaudio

# Configuration
CHUNK = 1024             # Frames per buffer
FORMAT = pyaudio.paInt16 # 16-bit res
CHANNELS = 1             # Mono
RATE = 16000             # Sampling rate

class AudioCapture:
    def __init__(self):
        # Audio stream
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

    def start(self):
        self.stream.start_stream()

    def read(self):
        return self.stream.read(CHUNK, exception_on_overflow=False)

    def shutdown(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()