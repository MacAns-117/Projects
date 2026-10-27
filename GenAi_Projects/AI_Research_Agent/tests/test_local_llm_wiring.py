"""Research agent wiring with an OpenAI-compatible (local) model — no network."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src import llm as llm_mod

LOCAL = {
    "LLM_PROVIDER": "openai_compatible",
    "LLM_BASE_URL": "http://localhost:8080/v1",
    "LLM_MODEL": "qwen-local",
}


@pytest.fixture
def local_env(monkeypatch):
    llm_mod._build.cache_clear()
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    for k, v in LOCAL.items():
        monkeypatch.setenv(k, v)
    yield
    llm_mod._build.cache_clear()


def test_validate_config_local_needs_only_tavily(local_env, monkeypatch):
    import src.config as cfg

    monkeypatch.setattr(cfg, "TAVILY_API_KEY", "tvly-test")
    cfg.validate_config()  # no GROQ_API_KEY needed


def test_validate_config_groq_default_still_needs_key(monkeypatch):
    import src.config as cfg

    for k in ("LLM_PROVIDER", "LLM_MODEL", "GROQ_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(cfg, "TAVILY_API_KEY", "tvly-test")
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        cfg.validate_config()


def test_orchestrator_builds_with_local_default(local_env):
    from langchain_openai import ChatOpenAI

    from src.orchestrator import create_orchestrator

    assert isinstance(llm_mod.get_llm(), ChatOpenAI)
    assert create_orchestrator() is not None


def test_summarizer_uses_smaller_cap(local_env):
    from src.tools.summarize_tools import get_summarizer

    chain = get_summarizer()
    model = chain.last
    assert model._get_request_payload([("user", "x")])["extra_body"] == {"max_tokens": 1024}


def test_planner_parses_list_after_reasoning_block():
    from src.agents.planner import plan_searches

    llm = MagicMock()
    fake = MagicMock()
    fake.invoke.return_value = MagicMock(
        content='<think>Let me plan ["not", "this"]</think>\n["q one", "q two", "q three"]'
    )
    from unittest.mock import patch

    with patch("src.agents.planner.create_planner", return_value=fake):
        assert plan_searches("question?", llm=llm) == ["q one", "q two", "q three"]


def test_eval_key_check_is_provider_aware(local_env, monkeypatch):
    import importlib

    run_eval = importlib.import_module("eval.run_eval")
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    assert run_eval._has_api_keys() is False
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
    assert run_eval._has_api_keys() is True
