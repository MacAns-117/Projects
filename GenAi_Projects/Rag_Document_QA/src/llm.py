"""Groq chat wrapper. Default model is openai/gpt-oss-120b on the free tier."""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.config import LLM_MAX_TOKENS, LLM_MODEL, LLM_TEMPERATURE

load_dotenv()


@lru_cache(maxsize=1)
def get_llm(
    model: str = LLM_MODEL,
    temperature: float = LLM_TEMPERATURE,
    max_tokens: int = LLM_MAX_TOKENS,
) -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Get a free key at https://console.groq.com/ "
            "and put it in .env as GROQ_API_KEY=..."
        )
    return ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        groq_api_key=api_key,
    )


def generate_answer(prompt: str, llm: ChatGroq | None = None) -> str:
    if llm is None:
        llm = get_llm()
    return llm.invoke(prompt).content
