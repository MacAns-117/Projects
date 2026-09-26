"""
Planner Agent — decomposes a research question into a search strategy.

Takes a broad question and generates specific search queries.
This is the first step in the multi-agent research pipeline.
"""

from __future__ import annotations

import json
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src.config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS


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


def create_planner(llm: ChatGroq | None = None):
    """Create a planner chain.

    Args:
        llm: An existing ChatGroq instance (optional — saves init time).

    Returns:
        A runnable chain that takes a question and returns search queries.
    """
    if llm is None:
        llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )

    prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)
    chain = prompt | llm
    return chain


def plan_searches(
    question: str,
    llm: ChatGroq | None = None,
    context: str = "",
) -> list[str]:
    """Decompose a research question into specific search queries.

    Args:
        question: The user's research question.
        llm: An existing ChatGroq instance (optional).
        context: Optional prior conversation context for follow-ups.

    Returns:
        List of 3-5 search query strings. Falls back to [question] if empty.
    """
    chain = create_planner(llm)
    response = chain.invoke({"question": question, "context": context or "(none)"})
    raw_output = response.content.strip()

    # The LLM might wrap in markdown code blocks or add extra text.
    # We try to extract the JSON list robustly.
    try:
        # Try direct parse first
        queries = json.loads(raw_output)
    except json.JSONDecodeError:
        # Try to find a JSON list in the text
        match = re.search(r'\[.*?\]', raw_output, re.DOTALL)
        if match:
            try:
                queries = json.loads(match.group(0))
            except json.JSONDecodeError:
                queries = []
        else:
            # Fallback: split by newlines and clean up
            queries = [
                line.strip().strip('"').strip("'").strip(",")
                for line in raw_output.split("\n")
                if line.strip() and not line.strip().startswith(("#", "//", "```"))
            ]

    # Ensure we have strings
    queries = [str(q) for q in queries if q]

    # If parsing yielded nothing usable, fall back to the original question
    if not queries:
        queries = [question]

    return queries


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
