import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ─────────────────────────────────────────────
# Project Paths
# ─────────────────────────────────────────────

# src/ directory → go two levels up to project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Folder containing .txt phrase files
TXT_INPUT_DIR = PROJECT_ROOT / "Txts"

# Folder where audio output will be stored
OUTPUT_ROOT = PROJECT_ROOT / "lesson_output"

# Default lesson file
DEFAULT_LESSON_FILE = TXT_INPUT_DIR / "text1.txt"

# ─────────────────────────────────────────────
# Audio / TTS Settings
# ─────────────────────────────────────────────
###voices = [
#    "alloy", "echo"(M), "fable"(B), "onyx"(M), "nova"(Good), "shimmer",
#    "coral", "verse", "ballad", "ash", "sage", "marin", "cedar"
#]
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TTS_VOICE = "onyx"

# Silence between joined phrases (ms)
SILENCE_BETWEEN_PHRASES_MS = 3500

# Slow audio factor (0.85 = 15% slower)
SLOW_FACTOR = 0.85
