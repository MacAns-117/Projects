"""Paths, model name, and caps. Change a value here, it is used everywhere."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_CSV = DATA_DIR / "hotel_bookings.csv"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "openai/gpt-oss-120b"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 2048

MAX_ITERATIONS = 6
MEMORY_WINDOW = 10

# Upload / load caps — this is a local demo, not a hosted warehouse.
MAX_UPLOAD_MB = 50
MAX_ROWS = 200_000
SQL_ROW_CAP = 200
CHART_POINT_CAP = 5_000

DROP_DUPLICATES = True


def validate_config(*, require_data: bool = True) -> None:
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found. Get a free key at https://console.groq.com/ "
            "and put it in .env as GROQ_API_KEY=..."
        )
    if require_data and not DEFAULT_CSV.exists():
        raise FileNotFoundError(
            f"Default sample CSV missing at {DEFAULT_CSV}. "
            "Add a CSV to data/ or upload one in the app."
        )
