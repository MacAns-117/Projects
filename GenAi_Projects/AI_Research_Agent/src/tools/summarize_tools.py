"""
Summarize tools — text summarization for the research agent.

Takes long text (e.g., an extracted web page) and summarizes it into
a concise paragraph. Used before synthesis to keep context windows manageable.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src.config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS


SUMMARIZE_PROMPT = """Summarize the following text into a concise paragraph (3-5 sentences).

Focus on:
1. The main point or argument
2. Key data points or facts mentioned
3. Any conclusions or recommendations

Text to summarize:
{text}

Summary:"""


def get_summarizer(llm: ChatGroq | None = None):
    """Create a summarization chain.

    Args:
        llm: An existing ChatGroq instance (optional — saves init time).

    Returns:
        A runnable chain that takes text and returns a summary.
    """
    if llm is None:
        llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=1024,  # Summaries don't need 4096 tokens
        )

    prompt = ChatPromptTemplate.from_template(SUMMARIZE_PROMPT)
    chain = prompt | llm
    return chain


def summarize_text(text: str, llm: ChatGroq | None = None, max_input_chars: int = 10000) -> str:
    """Summarize a block of text into a concise paragraph.

    Args:
        text: The text to summarize.
        llm: An existing ChatGroq instance (optional).
        max_input_chars: Truncate input to this many chars to avoid context overflow.

    Returns:
        A 3-5 sentence summary string.
    """
    if not text or len(text.strip()) < 50:
        return "No substantial text to summarize."

    # Truncate very long texts to avoid context window issues
    if len(text) > max_input_chars:
        text = text[:max_input_chars] + "\n[...truncated...]"
        print(f"  Input truncated to {max_input_chars} chars for summarization.")

    chain = get_summarizer(llm)
    response = chain.invoke({"text": text})
    return response.content


def summarize_multiple(texts: dict[str, str], llm: ChatGroq | None = None) -> dict[str, str]:
    """Summarize multiple text blocks.

    Args:
        texts: Dict mapping source URL/ID to text.
        llm: An existing ChatGroq instance (optional).

    Returns:
        Dict mapping source URL/ID to summary.
    """
    summaries = {}
    for source_id, text in texts.items():
        print(f"  Summarizing: {source_id[:60]}...")
        summaries[source_id] = summarize_text(text, llm)
    return summaries


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.config import validate_config

    print("Testing summarize_tools...\n")
    validate_config()

    # Simulate a long text
    long_text = """
    Retrieval-augmented generation (RAG) is an AI framework that retrieves facts from an external knowledge base
    to ground large language models (LLMs) on the most accurate, up-to-date information. RAG works by first
    taking an input query and searching a connected knowledge base for relevant information. The retrieved
    information is then appended to the user's prompt and passed to the LLM, which generates the final output.
    This approach helps reduce hallucinations, as the model can cite its sources directly from the retrieved context.
    Key challenges in RAG include chunking strategy, embedding model selection, and retrieval quality evaluation.
    Metrics like Hit@K, faithfulness, and answer relevance are used to measure RAG system performance.
    """ * 5  # Repeat to make it longer

    print(f"Input length: {len(long_text)} chars\n")
    summary = summarize_text(long_text)
    print(f"Summary ({len(summary)} chars):\n{summary}")