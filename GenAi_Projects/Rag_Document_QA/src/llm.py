"""
LLM module — wraps Groq's Llama 3.1 8B model with LangChain.

This is the "brain" of the RAG system — it takes the user's question
plus the retrieved context chunks and generates a natural-language
answer with citations.

The model is cached after first initialization (~1 sec). Subsequent
calls reuse the cached instance.

Requires GROQ_API_KEY environment variable (loaded from .env).
Get a free key at https://console.groq.com/
"""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Load environment variables from .env file
load_dotenv()

# Model configuration — Llama 3.1 8B Instant is fast and free on Groq
DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_TEMPERATURE = 0.1        # low = focused, deterministic answers
DEFAULT_MAX_TOKENS = 1024        # ~500-700 words, enough for most answers


@lru_cache(maxsize=1)
def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    max_tokens: int = DEFAULT_MAX_TOKENS,
) -> ChatGroq:
    """Get a cached ChatGroq LLM instance.

    Args:
        model: Groq model name (default: llama-3.1-8b-instant).
        temperature: 0 = deterministic, 1 = creative. Default 0.1 for
                     focused, factual RAG answers.
        max_tokens: Max length of generated answer.

    Returns:
        ChatGroq instance ready for invoke().

    Raises:
        ValueError: If GROQ_API_KEY is not set in environment.

    Why lru_cache(maxsize=1):
        First call initializes the ChatGroq client (~1 sec).
        All future calls return the cached instance.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Get a free key at https://console.groq.com/ "
            "and add it to your .env file: GROQ_API_KEY=your_key_here"
        )

    print(f"Initializing LLM: {model} (temp={temperature})...")
    llm = ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        groq_api_key=api_key,
    )
    print(f"  ✓ LLM ready ({model})")
    return llm


def generate_answer(
    prompt: str,
    llm: ChatGroq | None = None,
) -> str:
    """Generate an answer from a prompt using the LLM.

    Args:
        prompt: The full prompt including context and question.
        llm: An existing ChatGroq instance (optional — saves
             initialization if you already have one).

    Returns:
        The LLM's generated answer as a string.
    """
    if llm is None:
        llm = get_llm()

    response = llm.invoke(prompt)
    return response.content


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    print("Testing LLM module...\n")

    # Test 1: simple generation (no RAG context)
    print("--- Test 1: simple generation ---")
    simple_prompt = (
        "What is 2 + 2? Answer with just the number."
    )
    print(f"Prompt: {simple_prompt}")
    answer = generate_answer(simple_prompt)
    print(f"Answer: {answer}\n")

    # Test 2: RAG-style generation with context
    print("--- Test 2: RAG-style generation with context ---")
    context = (
        "[1] python_basics.pdf, p.1\n"
        "Python is a high-level programming language known for its readable syntax.\n\n"
        "[2] python_basics.pdf, p.2\n"
        "Lists in Python are ordered, mutable, and can hold mixed data types."
    )
    question = "What is Python?"
    rag_prompt = f"""Answer the question using ONLY the context below.
If the context doesn't contain the answer, say "I don't know based on the provided context."

Context:
{context}

Question: {question}

Answer (cite sources like [1], [2] when relevant):"""

    print(f"Question: {question}")
    print(f"Context: {context[:100]}...\n")
    answer = generate_answer(rag_prompt)
    print(f"Answer: {answer}")
    print(f"\n→ Answer should mention Python and cite [1].")