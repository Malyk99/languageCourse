from pathlib import Path
from pydub import AudioSegment

class AudioPostProcessor:
    def insert_silence(self, files, output, ms_silence=1500):
        """
        Classic mode:
        Inserts a fixed amount of silence (ms_silence) between each file.
        """
        combined = AudioSegment.silent(duration=0)
        silence = AudioSegment.silent(duration=ms_silence)

        for f in files:
            combined += AudioSegment.from_file(f) + silence

        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output, format="mp3")
        return output

    def insert_dynamic_silence(self, files, output, extra_ms=1000):
        """
        Dynamic mode:
        For each phrase, inserts silence whose duration is:
            (length of the previous phrase in ms) + extra_ms

        So if phrase_1 is 2500 ms, the pause after it will be:
            2500 + extra_ms  (e.g., 1000) = 3500 ms

        This gives longer pauses after longer phrases.
        """
        combined = AudioSegment.silent(duration=0)
        previous_len = None

        for f in files:
            audio = AudioSegment.from_file(f)
            combined += audio

            # Compute silence based on current phrase length
            previous_len = len(audio)  # duration in ms
            pause = AudioSegment.silent(duration=previous_len + extra_ms)
            combined += pause

        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output, format="mp3")
        return output
