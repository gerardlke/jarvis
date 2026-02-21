import audioop

class AudioDetector:

    def __init__(self):
        self.avg_energy = 0
        self.alpha = 0.1

        self.speaking = False
        self.speaking_threshold = 2.0  # How much audio needs to exceed average to start
        self.stopping_threshold = 1.5  # How much audio needs to exceed average to stop

        self.min_frames_to_start = 30  # Number of frames to calculate initial average 
        self.min_frames_to_stop = 1 / self.alpha
        self.cur_frames_to_stop = self.min_frames_to_stop
    
    def update(self, frame):
        energy = audioop.rms(frame, 2)

        # Only update average when not speaking
        if not self.speaking:
            self.avg_energy = (
                self.alpha * energy +
                (1 - self.alpha) * self.avg_energy
            )

        # If the initial audio threshold is done
        if self.min_frames_to_start == 0:
            start_threshold = self.avg_energy * self.speaking_threshold
            stop_threshold = self.avg_energy * self.stopping_threshold

            if not self.speaking and energy > start_threshold:
                # When user starts speaking, start countdown
                self.speaking = True
                self.cur_frames_to_stop = self.min_frames_to_stop

            elif self.speaking and energy < stop_threshold:
                # When speaking, countdown  number of frames below threshold before stopping
                self.cur_frames_to_stop -= 1
                if self.cur_frames_to_stop < 0:
                    self.speaking = False

            return self.speaking
        else:
            self.min_frames_to_start -= 1
            if self.min_frames_to_start == 0:
                print("Completed initial audio threshold calibrations.")
            return False