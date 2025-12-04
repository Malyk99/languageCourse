from pathlib import Path
import os
from openai import OpenAI

# Voices currently supported by gpt-4o-mini-tts:
# alloy, echo, fable, onyx, nova, shimmer,
# coral, verse, ballad, ash, sage, marin, cedar

class TTSEngine:
    def __init__(self, api_key: str | None = None,
                 model: str = "gpt-4o-mini-tts",
                 voice: str = "marin"):
        """
        Basic TTS wrapper around OpenAI's /audio/speech endpoint.
        - model: e.g. "gpt-4o-mini-tts"
        - voice: any of the supported voice names
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.voice = voice

    def synthesize(self, text: str, filename: str | Path, voice: str | None = None) -> Path:
        """
        Generate speech from `text` and save to `filename`.

        - `voice` parameter overrides the default voice if provided.
        - Returns the Path to the created file.
        """
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        chosen_voice = voice or self.voice
        print(f"Generating {filename.name} with voice='{chosen_voice}'...")

        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=chosen_voice,
                input=text,
                #instructions="Speak clearly and naturally.",
            )

            audio_bytes = response.read()

            with open(filename, "wb") as f:
                f.write(audio_bytes)

            print(f"Saved {filename}")
            return filename

        except Exception as e:
            print(f"[TTSEngine] ERROR while generating {filename.name}: {e}")
            raise
