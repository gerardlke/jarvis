import whisper

class SRModel:
    def __init__(self, model="base"):
        self.model = whisper.load_model(model)

    def transcribe(self, audio):
        audio = whisper.pad_or_trim(audio)

        # Make log-Mel spectrogram and move to same device as model
        mel = whisper.log_mel_spectrogram(
            audio,
            n_mels=self.model.dims.n_mels
        ).to(self.model.device)
        
        # Decode audio
        options = whisper.DecodingOptions(language="en", fp16=False)
        result = whisper.decode(self.model, mel, options)
        return result.text