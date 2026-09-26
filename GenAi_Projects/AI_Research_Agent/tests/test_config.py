"""Tests for config and gold questions file."""
import json
from pathlib import Path

from src.config import LLM_MODEL, LLM_TEMPERATURE, MAX_SOURCES, MEMORY_WINDOW

GOLD_FILE = Path(__file__).resolve().parent.parent / "eval" / "gold_questions.json"


class TestConfig:
    def test_llm_model_set(self):
        assert LLM_MODEL is not None
        assert isinstance(LLM_MODEL, str)

    def test_llm_temperature_range(self):
        assert 0 <= LLM_TEMPERATURE <= 1.0

    def test_max_sources_positive(self):
        assert isinstance(MAX_SOURCES, int)
        assert MAX_SOURCES > 0

    def test_memory_window_positive(self):
        assert isinstance(MEMORY_WINDOW, int)
        assert MEMORY_WINDOW > 0


class TestGoldQuestions:
    def test_file_exists(self):
        assert GOLD_FILE.exists()

    def test_has_15_questions(self):
        with open(GOLD_FILE) as f:
            questions = json.load(f)
        assert len(questions) == 15

    def test_unique_ids(self):
        with open(GOLD_FILE) as f:
            questions = json.load(f)
        ids = [q["id"] for q in questions]
        assert len(ids) == len(set(ids))

    def test_all_have_expected_phrases(self):
        with open(GOLD_FILE) as f:
            questions = json.load(f)
        for q in questions:
            assert "expected_phrases" in q
            assert len(q["expected_phrases"]) > 0
