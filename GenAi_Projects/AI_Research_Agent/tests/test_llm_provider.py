"""Provider selection for the chat model — no network, no real keys."""

from __future__ import annotations

import pytest

from src import llm as llm_mod
from src.llm import (
    DEFAULT_LLM_MODEL,
    DEFAULT_LOCAL_BASE_URL,
    DUMMY_API_KEY,
    get_llm,
    llm_label,
    resolve_llm_settings,
    strip_reasoning,
    validate,
)

LOCAL = {
    "LLM_PROVIDER": "openai_compatible",
    "LLM_BASE_URL": "http://localhost:8080/v1/",
    "LLM_MODEL": "qwen-local",
}


@pytest.fixture(autouse=True)
def _fresh_cache():
    llm_mod._build.cache_clear()
    yield
    llm_mod._build.cache_clear()


def test_default_is_groq_with_gpt_oss():
    s = resolve_llm_settings({})
    assert s.provider == "groq"
    assert s.model == DEFAULT_LLM_MODEL == "openai/gpt-oss-120b"
    assert s.base_url is None
    assert s.api_key is None


def test_groq_reads_key_and_model_override():
    s = resolve_llm_settings({"GROQ_API_KEY": "gsk_test", "LLM_MODEL": "llama-3.3-70b-versatile"})
    assert s.provider == "groq"
    assert s.api_key == "gsk_test"
    assert s.model == "llama-3.3-70b-versatile"


@pytest.mark.parametrize("alias", ["openai_compatible", "OpenAI-Compatible", "openai", "local"])
def test_provider_aliases(alias):
    s = resolve_llm_settings({**LOCAL, "LLM_PROVIDER": alias})
    assert s.provider == "openai_compatible"


def test_unknown_provider_rejected():
    with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
        resolve_llm_settings({"LLM_PROVIDER": "anthropic"})


def test_openai_compatible_requires_model():
    with pytest.raises(ValueError, match="LLM_MODEL is required"):
        resolve_llm_settings({"LLM_PROVIDER": "openai_compatible"})


def test_openai_compatible_defaults_and_dummy_key():
    s = resolve_llm_settings({"LLM_PROVIDER": "openai_compatible", "LLM_MODEL": "m"})
    assert s.base_url == DEFAULT_LOCAL_BASE_URL == "http://localhost:8080/v1"
    assert s.api_key == DUMMY_API_KEY
    # Groq key must not leak to a local server.
    s2 = resolve_llm_settings(
        {"LLM_PROVIDER": "openai_compatible", "LLM_MODEL": "m", "GROQ_API_KEY": "gsk_secret"}
    )
    assert s2.api_key == DUMMY_API_KEY


def test_openai_compatible_custom_values_and_secret_not_in_repr():
    s = resolve_llm_settings({**LOCAL, "LLM_API_KEY": "sk-local-123", "LLM_MAX_TOKENS": "8192"})
    assert s.base_url == "http://localhost:8080/v1"  # trailing slash stripped
    assert s.model == "qwen-local"
    assert s.api_key == "sk-local-123"
    assert s.max_tokens == 8192
    assert "sk-local-123" not in repr(s)
    assert "sk-local-123" not in s.label


@pytest.mark.parametrize("bad", ["abc", "0", "-5"])
def test_bad_max_tokens_rejected(bad):
    with pytest.raises(ValueError, match="LLM_MAX_TOKENS"):
        resolve_llm_settings({**LOCAL, "LLM_MAX_TOKENS": bad})


def test_bad_timeout_rejected():
    with pytest.raises(ValueError, match="LLM_TIMEOUT"):
        resolve_llm_settings({**LOCAL, "LLM_TIMEOUT": "soon"})


def test_validate_groq_needs_key_but_local_does_not():
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        validate({})
    assert validate(LOCAL).provider == "openai_compatible"


def test_llm_label_never_raises():
    assert "Groq" in llm_label({})
    assert "qwen-local" in llm_label(LOCAL)
    assert "localhost:8080" in llm_label(LOCAL)
    assert llm_label({"LLM_PROVIDER": "nope"}).startswith("misconfigured")


def test_get_llm_groq_default_builds_chatgroq():
    from langchain_groq import ChatGroq

    m = get_llm(env={"GROQ_API_KEY": "gsk_test"})
    assert isinstance(m, ChatGroq)
    assert m.model_name == DEFAULT_LLM_MODEL


def test_get_llm_groq_without_key_raises():
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        get_llm(env={})


def test_get_llm_openai_compatible_builds_chatopenai():
    from langchain_openai import ChatOpenAI

    m = get_llm(temperature=0.2, max_tokens=321, env=LOCAL)
    assert isinstance(m, ChatOpenAI)
    assert m.model_name == "qwen-local"
    assert m.openai_api_base == "http://localhost:8080/v1"
    assert m.openai_api_key.get_secret_value() == DUMMY_API_KEY
    payload = m._get_request_payload([("user", "hi")])
    # Classic max_tokens (understood by llama.cpp / Ollama / LM Studio) via extra_body.
    assert payload["extra_body"] == {"max_tokens": 321}
    assert "max_completion_tokens" not in payload
    assert payload["temperature"] == 0.2


def test_llm_max_tokens_env_overrides_call_default():
    m = get_llm(max_tokens=100, env={**LOCAL, "LLM_MAX_TOKENS": "4096"})
    assert m._get_request_payload([("user", "hi")])["extra_body"] == {"max_tokens": 4096}


def test_openai_compatible_supports_tool_binding():
    from langchain_core.tools import tool

    @tool
    def add(a: int, b: int) -> int:
        """Add two ints."""
        return a + b

    m = get_llm(env=LOCAL)
    bound = m.bind_tools([add])
    payload = m._get_request_payload([("user", "2+2?")], **bound.kwargs)
    assert payload["tools"][0]["function"]["name"] == "add"


def test_get_llm_reads_os_environ_by_default(monkeypatch):
    for k in LOCAL:
        monkeypatch.setenv(k, LOCAL[k])
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    from langchain_openai import ChatOpenAI

    assert isinstance(get_llm(), ChatOpenAI)


def test_strip_reasoning():
    assert strip_reasoning("<think>hmm\nlong</think>\nAnswer [1].") == "Answer [1]."
    assert strip_reasoning("Answer.") == "Answer."
    assert strip_reasoning("<think>cut off by token cap") == ""
    assert strip_reasoning("") == ""
    assert strip_reasoning(None) is None
