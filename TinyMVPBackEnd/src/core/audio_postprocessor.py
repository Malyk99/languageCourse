from pathlib import Path
from pydub import AudioSegment

class AudioPostProcessor:
    """
    Upgraded processor with support for:
      - classic silence
      - dynamic silence
      - spanish-only silence profile (¿¿ phrases)
      - stitching multiple audio sections in order
    """

    # ----------------------------------------
    # CLASSIC MODE (unchanged)
    # ----------------------------------------
    def insert_silence(self, files, output, ms_silence=1500):
        combined = AudioSegment.silent(duration=0)
        silence = AudioSegment.silent(duration=ms_silence)

        for f in files:
            combined += AudioSegment.from_file(f) + silence

        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output, format="mp3")
        return output

    # ----------------------------------------
    # DYNAMIC SILENCE (unchanged)
    # ----------------------------------------
    def insert_dynamic_silence(self, files, output, extra_ms=1000):
        combined = AudioSegment.silent(duration=0)

        for f in files:
            audio = AudioSegment.from_file(f)
            combined += audio
            pause = AudioSegment.silent(duration=len(audio) + extra_ms)
            combined += pause

        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output, format="mp3")
        return output

    # ----------------------------------------
    # NEW: Spanish-only silence profile
    # For ¿¿ phrases
    # ----------------------------------------
    def insert_silence_spanish(self, files, output, ms_silence=2200):
        """
        Inserts a separate silence profile for Spanish-only
        ¿¿ phrases. Default = 2.2 seconds.
        """
        combined = AudioSegment.silent(duration=0)
        silence = AudioSegment.silent(duration=ms_silence)

        for f in files:
            combined += AudioSegment.from_file(f) + silence

        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output, format="mp3")
        return output

    # ----------------------------------------
    # NEW: fully generic "silence profile" system
    # ----------------------------------------
    def insert_silence_with_profile(self, files, output, silence_ms):
        """
        General-purpose silence insertion.
        Used internally by spanish or normal TTS groups.
        """
        combined = AudioSegment.silent(duration=0)
        silence = AudioSegment.silent(duration=silence_ms)

        for f in files:
            combined += AudioSegment.from_file(f) + silence

        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output, format="mp3")
        return output

    # ----------------------------------------
    # NEW: Combine multiple "sections"
    # e.g., [spanish_intro_audio, main_lesson_audio]
    # ----------------------------------------
    def insert_sections(self, audio_files, output):
        """
        Concatenates fully-rendered audio sections in order.
        audio_files = list of MP3 file paths
        """
        combined = AudioSegment.silent(duration=0)

        for f in audio_files:
            combined += AudioSegment.from_file(f)

        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        combined.export(output, format="mp3")
        return output

    # ----------------------------------------
    # Slow down 
    # ----------------------------------------
    def slow_down(self, input_file, output_file, factor=0.85):
        input_file = Path(input_file)
        output_file = Path(output_file)

        audio = AudioSegment.from_file(input_file)

        slowed = audio._spawn(
            audio.raw_data,
            overrides={"frame_rate": int(audio.frame_rate * factor)}
        ).set_frame_rate(audio.frame_rate)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        slowed.export(output_file, format=output_file.suffix.lstrip("."))
        return output_file
