"""LLM provider selection for RAG Document QA.

Default is Groq (``LLM_PROVIDER=groq``), so existing setups and the hosted demo
behave exactly as before. Set ``LLM_PROVIDER=openai_compatible`` to point the
app at any OpenAI-compatible server instead (llama.cpp ``llama-server``,
Ollama, LM Studio, vLLM, ...).

Environment variables (read when the model is built, not at import):

    LLM_PROVIDER     groq (default) | openai_compatible
    LLM_MODEL        model id. Optional for groq (default openai/gpt-oss-120b),
                     required for openai_compatible.
    LLM_BASE_URL     OpenAI-compatible base URL, default http://localhost:8080/v1
                     (only used by openai_compatible)
    LLM_API_KEY      bearer token for openai_compatible. Optional; local servers
                     usually ignore it, so a dummy value is sent if unset.
    LLM_MAX_TOKENS   optional override of the per-call output cap (handy for
                     local "thinking" models whose reasoning counts against it).
    LLM_TIMEOUT      optional request timeout in seconds for openai_compatible
                     (default 300; local CPU/GPU generation can be slow).
    GROQ_API_KEY     required for groq.

This file is intentionally self-contained (each app deploys on its own), so the
same small helper is duplicated in the three GenAI apps rather than shared.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Mapping

from dotenv import load_dotenv

from src.config import DEFAULT_LLM_MODEL, LLM_MAX_TOKENS, LLM_TEMPERATURE

load_dotenv()

DEFAULT_LOCAL_BASE_URL = "http://localhost:8080/v1"
DUMMY_API_KEY = "not-needed"
PROVIDERS = ("groq", "openai_compatible")
_ALIASES = {
    "": "groq",
    "groq": "groq",
    "openai_compatible": "openai_compatible",
    "openai-compatible": "openai_compatible",
    "openai": "openai_compatible",
    "local": "openai_compatible",
}


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    model: str
    base_url: str | None = None
    # repr=False so a settings object never prints a key into logs.
    api_key: str | None = field(default=None, repr=False)
    max_tokens: int | None = None
    timeout: float = 300.0

    @property
    def label(self) -> str:
        if self.provider == "groq":
            return f"{self.model} (Groq)"
        return f"{self.model} (OpenAI-compatible @ {self.base_url})"


def _clean(value: str | None) -> str:
    return (value or "").strip()


def resolve_llm_settings(env: Mapping[str, str] | None = None) -> LLMSettings:
    """Read provider settings from ``env`` (defaults to ``os.environ``).

    Raises ValueError for an unknown provider, a missing LLM_MODEL in
    openai_compatible mode, or a non-integer LLM_MAX_TOKENS. Does not check
    GROQ_API_KEY; ``get_llm`` / ``validate`` do that.
    """
    env = os.environ if env is None else env
    raw = _clean(env.get("LLM_PROVIDER")).lower()
    provider = _ALIASES.get(raw)
    if provider is None:
        raise ValueError(
            f"Unknown LLM_PROVIDER={raw!r}. Use one of: {', '.join(PROVIDERS)}."
        )

    max_tokens: int | None = None
    raw_max = _clean(env.get("LLM_MAX_TOKENS"))
    if raw_max:
        try:
            max_tokens = int(raw_max)
        except ValueError as exc:
            raise ValueError(f"LLM_MAX_TOKENS must be an integer, got {raw_max!r}") from exc
        if max_tokens <= 0:
            raise ValueError("LLM_MAX_TOKENS must be > 0")

    timeout = 300.0
    raw_timeout = _clean(env.get("LLM_TIMEOUT"))
    if raw_timeout:
        try:
            timeout = float(raw_timeout)
        except ValueError as exc:
            raise ValueError(f"LLM_TIMEOUT must be a number, got {raw_timeout!r}") from exc

    model = _clean(env.get("LLM_MODEL"))
    if provider == "groq":
        key = _clean(env.get("GROQ_API_KEY")) or None
        return LLMSettings("groq", model or DEFAULT_LLM_MODEL, None, key, max_tokens, timeout)

    if not model:
        raise ValueError(
            "LLM_MODEL is required when LLM_PROVIDER=openai_compatible "
            "(e.g. the model name your llama-server / Ollama / LM Studio serves)."
        )
    base_url = (_clean(env.get("LLM_BASE_URL")) or DEFAULT_LOCAL_BASE_URL).rstrip("/")
    key = _clean(env.get("LLM_API_KEY")) or DUMMY_API_KEY
    return LLMSettings("openai_compatible", model, base_url, key, max_tokens, timeout)


def validate(env: Mapping[str, str] | None = None) -> LLMSettings:
    """Resolve settings and check the provider has what it needs."""
    s = resolve_llm_settings(env)
    if s.provider == "groq" and not s.api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Get a free key at https://console.groq.com/ "
            "and put it in .env as GROQ_API_KEY=..., or set "
            "LLM_PROVIDER=openai_compatible to use a local model."
        )
    return s


def llm_label(env: Mapping[str, str] | None = None) -> str:
    """Human-readable 'model (provider)' for sidebars and /health. Never raises."""
    try:
        return resolve_llm_settings(env).label
    except ValueError as exc:
        return f"misconfigured: {exc}"


def get_llm(
    temperature: float = LLM_TEMPERATURE,
    max_tokens: int = LLM_MAX_TOKENS,
    env: Mapping[str, str] | None = None,
):
    """Return a LangChain chat model for the configured provider.

    groq              -> langchain_groq.ChatGroq (unchanged default behaviour)
    openai_compatible -> langchain_openai.ChatOpenAI(base_url=...)

    Both support ``.invoke`` and ``.bind_tools``, so prompt chains and
    tool-calling agents work with either. Imports are lazy so tests and
    eval scripts can import this module without either SDK configured.
    """
    s = validate(env)
    return _build(s, float(temperature), int(s.max_tokens or max_tokens))


@lru_cache(maxsize=8)
def _build(s: LLMSettings, temperature: float, cap: int):
    if s.provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=s.model,
            temperature=temperature,
            max_tokens=cap,
            groq_api_key=s.api_key,
        )

    from langchain_openai import ChatOpenAI

    # Send the classic ``max_tokens`` field: llama.cpp, Ollama and LM Studio all
    # honour it, whereas ChatOpenAI's own max_tokens is sent as
    # ``max_completion_tokens``, which some local servers ignore.
    return ChatOpenAI(
        model=s.model,
        base_url=s.base_url,
        api_key=s.api_key,
        temperature=temperature,
        extra_body={"max_tokens": cap},
        max_retries=1,
        timeout=s.timeout,
    )


_THINK_RE = re.compile(r"<think>.*?</think>\s*", re.DOTALL | re.IGNORECASE)


def strip_reasoning(text):
    """Drop ``<think>...</think>`` blocks some local reasoning models emit inline.

    llama-server normally moves reasoning into a separate field, but if a
    server/template leaves it in ``content`` we don't want it in answers or
    parsed output. An unterminated leading ``<think>`` (output cut off by the
    token cap) yields an empty string.
    """
    if not isinstance(text, str) or not text:
        return text
    out = _THINK_RE.sub("", text)
    if out.lstrip().lower().startswith("<think>"):
        return ""
    return text if out == text else out.strip()


def generate_answer(prompt: str, llm=None) -> str:
    if llm is None:
        llm = get_llm()
    content = llm.invoke(prompt).content
    return strip_reasoning(content if isinstance(content, str) else str(content))
