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

    parsed = parser.parse(raw_text)  
    phrases = parsed["phrases"]              # English/Spanish pairs
    spanish_spoken = parsed["spanish_spoken"]  # ¿¿ Spanish-only lines

    if not phrases and not spanish_spoken:
        print("No valid phrases found in file. Check your input format.")
        return

    # 2. Prepare output folders
    lesson_name = lesson_file.stem
    lesson_root = config.OUTPUT_ROOT / lesson_name
    normal_dir = lesson_root / "normal"
    spanish_dir = lesson_root / "spanish_intro"
    slow_dir = lesson_root / "slow"

    normal_dir.mkdir(parents=True, exist_ok=True)
    spanish_dir.mkdir(parents=True, exist_ok=True)
    slow_dir.mkdir(parents=True, exist_ok=True)

    # 3. Init TTS engine
    print("Initializing TTS engine...")
    tts = TTSEngine(
        model=config.DEFAULT_TTS_MODEL,
        voice=config.DEFAULT_TTS_VOICE,
        api_key=config.OPENAI_API_KEY,
    )
    post = AudioPostProcessor()

    # -----------------------------------------------------------
    # 4A. Generate English/Spanish per-phrase audio (main lesson)
    # -----------------------------------------------------------
    print("\nGenerating main lesson audio (normal speed)...")
    normal_files: list[Path] = []

    for idx, p in enumerate(phrases, start=1):
        text_en = p["en"]
        out_file = normal_dir / f"phrase_{idx:02d}.mp3"
        print(f" → Lesson phrase: {text_en} -> {out_file.name}")
        tts.synthesize(text_en, out_file)
        normal_files.append(out_file)

    # -----------------------------------------------------------
    # 4B. Generate Spanish-only intro section (¿¿ phrases)
    # -----------------------------------------------------------
    spanish_files: list[Path] = []

    if spanish_spoken:
        print("\nGenerating Spanish-only intro audio (¿¿ tagged phrases)...")
        for idx, p in enumerate(spanish_spoken, start=1):
            text_es = p["es"]
            out_file = spanish_dir / f"spanish_{idx:02d}.mp3"
            print(f" → Spanish phrase: {text_es} -> {out_file.name}")
            tts.synthesize(text_es, out_file)
            spanish_files.append(out_file)
    else:
        print("\nNo ¿¿ Spanish phrases found.")

    # -----------------------------------------------------------
    # 5. Post-processing: Silence profiles for both sections
    # -----------------------------------------------------------
    # Spanish intro section with its own silence
    spanish_section_file = lesson_root / "section_spanish_intro.mp3"

    if spanish_files:
        print(
            f"\nBuilding Spanish intro section with "
            f"{config.SILENCE_SPANISH_SECTION_MS} ms silence..."
        )
        post.insert_silence_spanish(
            [str(f) for f in spanish_files],
            spanish_section_file,
            ms_silence=config.SILENCE_SPANISH_SECTION_MS,
        )
    else:
        # If no spanish section, create an empty file
        spanish_section_file = None

    # Main lesson section
    lesson_section_file = lesson_root / "section_main_lesson.mp3"
    print(
        f"Building main lesson section with "
        f"{config.SILENCE_BETWEEN_PHRASES_MS} ms silence..."
    )
    post.insert_silence(
        [str(f) for f in normal_files],
        lesson_section_file,
        ms_silence=config.SILENCE_BETWEEN_PHRASES_MS,
    )

    # -----------------------------------------------------------
    # 6. Combine Spanish section + Main lesson into full_normal
    # -----------------------------------------------------------
    full_normal = lesson_root / "full_normal.mp3"
    print(f"\nCombining sections into: {full_normal.name}")

    sections_to_join = []
    if spanish_section_file:
        sections_to_join.append(spanish_section_file)
    sections_to_join.append(lesson_section_file)

    post.insert_sections(
        audio_files=[str(f) for f in sections_to_join],
        output=full_normal
    )

    # -----------------------------------------------------------
    # 7. Create slow version
    # -----------------------------------------------------------
    full_slow = lesson_root / "full_slow.mp3"
    print(f"Creating slow version {full_slow.name} (factor {config.SLOW_FACTOR})...")
    post.slow_down(full_normal, full_slow, factor=config.SLOW_FACTOR)

    # -----------------------------------------------------------
    # 8. Done
    # -----------------------------------------------------------
    print("\nDone!")
    print(f"Lesson output folder: {lesson_root}")
    print(" Files:")
    print(f"  - Spanish intro phrases: {spanish_dir}")
    print(f"  - Main lesson phrases:   {normal_dir}")
    print(f"  - Full normal:           {full_normal}")
    print(f"  - Full slow:             {full_slow}")


if __name__ == "__main__":
    main()
