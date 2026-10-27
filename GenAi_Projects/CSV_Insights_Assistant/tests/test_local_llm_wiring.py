"""CSV app wiring with an OpenAI-compatible (local) model — built, never called."""

from __future__ import annotations

import pytest

from src import llm as llm_mod
from src.routing import classify_intent

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


def test_validate_config_accepts_local_without_groq_key(local_env):
    from src.config import validate_config

    validate_config(require_data=False)


def test_validate_config_groq_default_still_needs_key(monkeypatch):
    from src.config import validate_config

    for k in ("LLM_PROVIDER", "LLM_MODEL", "GROQ_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        validate_config(require_data=False)


def test_tool_calling_agents_build_with_local_model(local_env, sales_df):
    from langchain_openai import ChatOpenAI

    from src.agents.data_analyst import create_data_analyst
    from src.chart_buffer import ChartBuffer
    from src.agents.viz_agent import create_viz_agent

    llm = llm_mod.get_llm()
    assert isinstance(llm, ChatOpenAI)
    analyst = create_data_analyst(sales_df, llm)
    viz = create_viz_agent(sales_df, ChartBuffer(), llm)
    assert {t.name for t in analyst.tools} >= {"tool_sql", "tool_aggregate"}
    assert {t.name for t in viz.tools} == {"tool_chart", "tool_compare_chart"}


def test_orchestrator_builds_with_local_default(local_env, sales_df):
    from src.orchestrator import create_orchestrator

    assert create_orchestrator(sales_df) is not None


def test_health_label_shows_local_model(local_env):
    assert "qwen-local" in llm_mod.llm_label()


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("<think>user wants a chart</think>\nviz", "viz"),
        ("<think>\nmulti\nline\n</think> both", "both"),
        ("general", "general"),
        ("<think>never closed", "data"),
    ],
)
def test_router_ignores_reasoning_blocks(raw, expected):
    assert classify_intent(raw) == expected
