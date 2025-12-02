# main.py

from pathlib import Path

from src.core.phrase_parser import PhraseParser
from src.core.tts_engine import TTSEngine
from src.core.audio_postprocessor import AudioPostProcessor
from src import config


def main():
    # 1. Read phrases from txt file
    lesson_file: Path = config.DEFAULT_LESSON_FILE
    print(f"Using lesson file: {lesson_file}")

    raw_text = lesson_file.read_text(encoding="utf-8")

    print("Parsing phrases...")
    parser = PhraseParser()
    phrases = parser.parse(raw_text)  # list of {"en": ..., "es": ..., "id": ...}

    if not phrases:
        print("No phrases found in file. Check the format: 'English / Spanish' per line.")
        return

    # 2. Prepare output folders
    lesson_name = lesson_file.stem  # e.g. "master_phrases"
    lesson_root = config.OUTPUT_ROOT / lesson_name
    normal_dir = lesson_root / "normal"
    slow_dir = lesson_root / "slow"

    normal_dir.mkdir(parents=True, exist_ok=True)
    slow_dir.mkdir(parents=True, exist_ok=True)

    # 3. Init TTS engine
    print("Initializing TTS engine...")
    tts = TTSEngine(
        model=config.DEFAULT_TTS_MODEL,
        voice=config.DEFAULT_TTS_VOICE,
        api_key=config.OPENAI_API_KEY,
    )
    post = AudioPostProcessor()

    # 4. Generate per-phrase audio (normal speed)
    print("Generating audio for each phrase (normal speed)...")
    normal_files: list[Path] = []

    for idx, p in enumerate(phrases, start=1):
        text_en = p["en"]
        out_file = normal_dir / f"phrase_{idx:02d}.mp3"
        print(f" → {text_en} -> {out_file.name}")
        tts.synthesize(text_en, out_file)
        normal_files.append(out_file)

    # 5. Create full lesson (normal)
    full_normal = lesson_root / "full_normal.mp3"
    print(
        f"\nCombining into {full_normal.name} "
        f"with {config.SILENCE_BETWEEN_PHRASES_MS} ms pauses..."
    )
    post.insert_silence(
        [str(p) for p in normal_files],
        full_normal,
        ms_silence=config.SILENCE_BETWEEN_PHRASES_MS,
    )


    # 6. Create slow version of full lesson
    full_slow = lesson_root / "full_slow.mp3"
    print(f"Creating slow version {full_slow.name} (factor {config.SLOW_FACTOR})...")
    post.slow_down(full_normal, full_slow, factor=config.SLOW_FACTOR)

    print("\nDone!")
    print(f"Lesson output folder: {lesson_root}")
    print(" Files:")
    print(f"  - Per phrase (normal): {normal_dir}")
    print(f"  - Full normal: {full_normal}")
    print(f"  - Full slow:   {full_slow}")


if __name__ == "__main__":
    main()
