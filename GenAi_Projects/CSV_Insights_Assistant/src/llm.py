"""Shared Groq client. Import is lazy so pytest can run without a key."""

from __future__ import annotations

from src.config import LLM_MAX_TOKENS, LLM_MODEL, LLM_TEMPERATURE, GROQ_API_KEY


def get_llm():
    from langchain_groq import ChatGroq

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY missing")
    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
    )
