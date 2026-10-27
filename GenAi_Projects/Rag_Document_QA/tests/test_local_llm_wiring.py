"""RAG generation + faithfulness judge with LLM_* provider vars — no network."""

from __future__ import annotations

import pytest

from eval.faithfulness import GROQ_OPENAI_BASE_URL, resolve_judge_settings
from src.llm import generate_answer

LOCAL = {
    "LLM_PROVIDER": "openai_compatible",
    "LLM_BASE_URL": "http://localhost:8080/v1",
    "LLM_MODEL": "qwen-local",
}


class _Msg:
    def __init__(self, content):
        self.content = content


class _FakeLLM:
    def __init__(self, content):
        self._content = content

    def invoke(self, _prompt):
        return _Msg(self._content)


def test_generate_answer_strips_reasoning():
    out = generate_answer("q", llm=_FakeLLM("<think>check chunk 1</think>\nN = 6 [1]."))
    assert out == "N = 6 [1]."


def test_judge_defaults_to_groq_with_groq_key():
    js = resolve_judge_settings({"GROQ_API_KEY": "gsk_test"})
    assert js.base_url == GROQ_OPENAI_BASE_URL
    assert js.model == "openai/gpt-oss-120b"
    assert js.api_key == "gsk_test"
    assert "gsk_test" not in repr(js)


def test_judge_reuses_local_llm_vars():
    js = resolve_judge_settings({**LOCAL, "GROQ_API_KEY": "gsk_secret"})
    assert js.base_url == "http://localhost:8080/v1"
    assert js.model == "qwen-local"
    assert js.api_key != "gsk_secret"  # Groq key never sent to a local server


def test_judge_model_override_with_local_vars():
    js = resolve_judge_settings({**LOCAL, "JUDGE_MODEL": "bigger-judge", "LLM_API_KEY": "k"})
    assert js.model == "bigger-judge"
    assert js.api_key == "k"


def test_judge_explicit_openai_base_wins():
    js = resolve_judge_settings(
        {
            **LOCAL,
            "OPENAI_BASE_URL": "http://127.0.0.1:9000/v1/",
            "OPENAI_API_KEY": "judge-key",
            "JUDGE_MODEL": "j",
        }
    )
    assert (js.base_url, js.model, js.api_key) == ("http://127.0.0.1:9000/v1", "j", "judge-key")


def test_judge_explicit_groq_base_falls_back_to_groq_key_only_for_groq_host():
    js = resolve_judge_settings(
        {"OPENAI_BASE_URL": GROQ_OPENAI_BASE_URL, "GROQ_API_KEY": "gsk_test"}
    )
    assert js.api_key == "gsk_test"
    js2 = resolve_judge_settings(
        {"OPENAI_BASE_URL": "http://127.0.0.1:8080/v1", "GROQ_API_KEY": "gsk_test"}
    )
    assert js2.api_key == "local"


def test_judge_max_tokens_follows_llm_max_tokens():
    assert resolve_judge_settings({**LOCAL}).max_tokens == 256
    assert resolve_judge_settings({**LOCAL, "LLM_MAX_TOKENS": "4096"}).max_tokens == 4096


def test_judge_unconfigured_raises():
    with pytest.raises(RuntimeError, match="No judge endpoint"):
        resolve_judge_settings({})
    with pytest.raises(RuntimeError, match="LLM_MODEL"):
        resolve_judge_settings({"LLM_PROVIDER": "openai_compatible"})


def test_default_judge_calls_openai_client_with_resolved_settings(monkeypatch):
    import openai

    import eval.faithfulness as f

    seen = {}

    class _Choice:
        message = type("M", (), {"content": '<think>x</think>{"grounded": true, "reason": "ok"}'})

    class _Completions:
        def create(self, **kw):
            seen.update(kw)
            return type("R", (), {"choices": [_Choice()]})

    class _Client:
        def __init__(self, base_url, api_key):
            seen["base_url"] = base_url
            seen["api_key"] = api_key
            self.chat = type("C", (), {"completions": _Completions()})

    for k, v in LOCAL.items():
        monkeypatch.setenv(k, v)
    for k in ("OPENAI_BASE_URL", "OPENAI_API_KEY", "JUDGE_MODEL", "LLM_MAX_TOKENS"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(openai, "OpenAI", _Client)
    raw = f.default_openai_judge("prompt")
    assert f.parse_judge_json(raw) == (True, "ok")
    assert seen["base_url"] == "http://localhost:8080/v1"
    assert seen["model"] == "qwen-local"
    assert seen["max_tokens"] == 256
