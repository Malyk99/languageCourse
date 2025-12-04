# generate_voice_previews.py
import json
from pathlib import Path
from src.core.voice_profiles import VOICE_PROFILES
from src.core.tts_engine import TTSEngine
from src import config

PREVIEW_TEXT = {
    "en": "Hello, this is a sample of the English teaching voice.",
    "es": "Hola, esta es una muestra de la voz de enseñanza en español."
}

def main():
    print("Generating voice previews...")
    
    base_dir = Path("voice_previews")
    (base_dir / "english").mkdir(parents=True, exist_ok=True)
    (base_dir / "spanish").mkdir(parents=True, exist_ok=True)

    preview_map = {}

    for name, profile in VOICE_PROFILES.items():
        lang = profile["language"]
        folder = "english" if lang == "en" else "spanish"
        out_path = base_dir / folder / f"{name}.mp3"

        tts = TTSEngine(
            model=profile["model"],
            voice=profile["voice"],
            api_key=config.OPENAI_API_KEY,
            #instructions=profile["instructions"]
        )

        print(f" → Generating preview for {name} -> {out_path}")
        tts.synthesize(PREVIEW_TEXT[lang], out_path)

        preview_map[name] = str(out_path)

    # Save mapping
    with open(base_dir / "previews.json", "w", encoding="utf-8") as f:
        json.dump(preview_map, f, indent=2, ensure_ascii=False)

    print("\nAll previews generated!")
    print("Preview files saved in /voice_previews")
    print("Mapping saved in previews.json")

if __name__ == "__main__":
    main()
