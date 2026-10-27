"""
Centralized configuration for the AI Research Agent.

All paths, API keys, model names, and search parameters live here.
Requires TAVILY_API_KEY plus an LLM: GROQ_API_KEY (default) or
LLM_PROVIDER=openai_compatible + LLM_MODEL for a local server (see src/llm.py).
"""

from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent  # project root

# --- LLM Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# LLM provider: see src/llm.py. Default Groq + gpt-oss-120b; LLM_PROVIDER /
# LLM_MODEL / LLM_BASE_URL / LLM_API_KEY switch to any OpenAI-compatible server.
DEFAULT_LLM_MODEL = "openai/gpt-oss-120b"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower() or "groq"
LLM_MODEL = os.getenv("LLM_MODEL", "").strip() or DEFAULT_LLM_MODEL
LLM_TEMPERATURE = 0.3               # Slightly higher than data analysis — allows creative search planning
LLM_MAX_TOKENS = 4096                # Larger for report generation

# --- Search Configuration ---
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
MAX_SEARCH_RESULTS = 5              # Max results per search query
SEARCH_DEPTH = "advanced"           # "basic" or "advanced" (advanced reads more content)
INCLUDE_ANSWER = True               # Tavily can generate a quick answer alongside results

# --- Agent Configuration ---
# Linear pipeline only (Planner → Searcher → Synthesizer → Report Writer); no retry loop.
MAX_SOURCES = 10                    # Max total sources to synthesize

# --- Memory ---
MEMORY_WINDOW = 10                  # Max messages in conversation history


def validate_config() -> None:
    """Validate that required config is present. Raises ValueError if not."""
    # Provider-aware: Groq needs GROQ_API_KEY; openai_compatible needs LLM_MODEL.
    from src.llm import validate as validate_llm

    validate_llm()
    if not TAVILY_API_KEY:
        raise ValueError(
            "TAVILY_API_KEY not found. "
            "Get a free key at https://tavily.com "
            "and add it to your .env file."
        )
