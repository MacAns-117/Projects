"""
Planner Agent — decomposes a research question into a search strategy.

Takes a broad question and generates specific search queries.
This is the first step in the multi-agent research pipeline.
"""

from __future__ import annotations

import json
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel

from src.llm import get_llm, strip_reasoning

MIN_QUERIES = 3
MAX_QUERIES = 5

PLANNER_PROMPT = """You are a research planning assistant.

Your job is to take a research question and break it down into a list of specific, targeted search queries.

Guidelines:
1. Generate 3 to 5 search queries.
2. Each query should be specific enough for a web search engine (not just keywords).
3. Cover different angles of the question (e.g., definitions, comparisons, recent developments, criticisms).
4. Do not duplicate queries.
5. If prior conversation context is provided, use it to resolve follow-ups (e.g. "that framework", "compare to the earlier metric").

Return ONLY a JSON list of strings. No explanation, no markdown.

Example:
Question: "What are the latest advances in RAG evaluation?"
Output: ["RAGAS evaluation framework for RAG systems", "faithfulness vs answer relevance metrics in RAG", "RAG evaluation benchmarks 2024 2025", "how to measure retrieval quality in RAG pipelines"]

Prior conversation context (may be empty):
{context}

Question: {question}

Output:"""


_FENCE_RE = re.compile(
    r"^```(?:json|JSON)?\s*\n?(.*?)\n?```\s*$",
    re.DOTALL,
)


def _strip_fences(text: str) -> str:
    """Remove a wrapping markdown code fence if present."""
    text = text.strip()
    m = _FENCE_RE.match(text)
    if m:
        return m.group(1).strip()
    # Partial fences (opening only / trailing only)
    text = re.sub(r"^```(?:json|JSON)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


def _message_text(content) -> str:
    """Normalize LLM message content to a plain string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and "text" in block:
                parts.append(str(block["text"]))
            else:
                parts.append(str(block))
        return "".join(parts)
    return str(content)


def parse_query_list(raw: str) -> list[str] | None:
    """Parse and validate planner output.

    Returns a list of 3–5 non-empty strings, or None if the payload is unusable.
    Never expands a JSON string into a list of characters.
    """
    if not raw or not str(raw).strip():
        return None

    cleaned = _strip_fences(str(raw))
    data = None
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        else:
            return None

    # A bare JSON string must not become list(str) → characters.
    if isinstance(data, str):
        return None
    if not isinstance(data, list):
        return None

    queries: list[str] = []
    for item in data:
        if not isinstance(item, str):
            return None
        s = item.strip()
        if not s:
            return None
        queries.append(s)

    if not (MIN_QUERIES <= len(queries) <= MAX_QUERIES):
        return None
    return queries


def create_planner(llm: BaseChatModel | None = None):
    """Create a planner chain.

    Args:
        llm: An existing chat model (Groq or OpenAI-compatible) (optional — saves init time).

    Returns:
        A runnable chain that takes a question and returns search queries.
    """
    if llm is None:
        llm = get_llm()

    prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
    chain = prompt | llm
    return chain


def plan_searches(
    question: str,
    llm: BaseChatModel | None = None,
    context: str = "",
) -> list[str]:
    """Decompose a research question into specific search queries.

    Tries the LLM up to twice. Accepts only a JSON list of 3–5 non-empty
    strings. On persistent bad output, falls back to ``[question]``.

    Args:
        question: The user's research question.
        llm: An existing chat model (Groq or OpenAI-compatible) (optional).
        context: Optional prior conversation context for follow-ups.

    Returns:
        List of 3-5 search query strings, or ``[question]`` as a last resort.
    """
    chain = create_planner(llm)
    fallback = [question]
    payload = {"question": question, "context": context or "(none)"}

    for _attempt in range(2):
        response = chain.invoke(payload)
        raw = strip_reasoning(_message_text(getattr(response, "content", response)))
        parsed = parse_query_list(raw)
        if parsed is not None:
            return parsed

    return fallback


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.config import validate_config

    print("Testing planner agent...\n")
    validate_config()

    question = "What are the latest advances in RAG evaluation?"
    print(f"Question: {question}\n")

    queries = plan_searches(question)
    print(f"Generated {len(queries)} search queries:")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")
