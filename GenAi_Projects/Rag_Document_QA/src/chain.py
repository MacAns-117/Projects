"""
Chain module — ties retriever + LLM into the end-to-end RAG pipeline.

This is where the RAG magic happens:
  1. User asks a question
  2. Retriever finds the top-K most relevant chunks
  3. Chunks are formatted into a context string with numbered citations
  4. A prompt is built: system instructions + context + question
  5. The LLM generates an answer grounded in the context
  6. The answer + citations are returned together

The prompt is carefully engineered to:
  - Force the LLM to use ONLY the retrieved context (no hallucination)
  - Require citations in [N] format matching the context numbering
  - Say "I don't know" honestly when the context doesn't contain the answer
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_chroma import Chroma

from src.llm import get_llm, generate_answer
from src.retriever import retrieve_with_context, RetrievedChunk
from src.vectorstore import DEFAULT_TOP_K


# The system prompt — carefully engineered for citation-grounded RAG
SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the context provided below.

Rules:
1. Use ONLY the information in the context to answer the question.
2. Look carefully through ALL the context before answering. The answer may be in any of the numbered chunks, not just the first one.
3. If the context truly does not contain the answer after careful review, say: "I don't know based on the provided context."
4. Cite your sources using [N] notation, where N matches the number in the context.
   Example: "Python is a high-level language [1]."
5. If multiple sources support a claim, cite all of them: "Lists are mutable [1][2]."
6. Do NOT make up information or use knowledge outside the context.
7. Keep answers concise and direct — no fluff, no preamble.

Context:
{context}

Question: {question}

Answer:"""


@dataclass
class RAGAnswer:
    """The complete result of a RAG query.

    Attributes:
        question: The user's original question.
        answer: The LLM's generated answer.
        citations: List of RetrievedChunk objects used as context.
        context_string: The formatted context string passed to the LLM.
    """
    question: str
    answer: str
    citations: list[RetrievedChunk]
    context_string: str


def ask(
    question: str,
    vectorstore: Chroma | None = None,
    db_path: str | None = None,
    top_k: int = DEFAULT_TOP_K,
) -> RAGAnswer:
    """Ask a question and get a cited answer.

    This is the main entry point for the RAG system. It:
      1. Retrieves the top-K relevant chunks
      2. Formats them as a numbered context string
      3. Builds a prompt with system instructions + context + question
      4. Calls the LLM to generate an answer
      5. Returns the answer + citations together

    Args:
        question: The user's natural-language question.
        vectorstore: An existing Chroma instance (optional — saves DB load).
        db_path: Path to persistent DB (used only if vectorstore is None).
        top_k: Number of chunks to retrieve (default 4).

    Returns:
        RAGAnswer object with question, answer, citations, and context.

    Raises:
        ValueError: If neither vectorstore nor db_path is provided.
    """
    if vectorstore is None and db_path is None:
        raise ValueError("Must provide either vectorstore or db_path")

    # Step 1 + 2: Retrieve chunks and format as context string
    print(f"\n  [1/3] Retrieving top-{top_k} chunks for: '{question[:50]}...'")
    citations, context_string = retrieve_with_context(
        question, vectorstore=vectorstore, db_path=db_path, top_k=top_k
    )

    if not citations:
        return RAGAnswer(
            question=question,
            answer="I don't know based on the provided context.",
            citations=[],
            context_string="No relevant context found.",
        )

    print(f"       Found {len(citations)} chunks")

    # Step 3: Build the full prompt
    print(f"  [2/3] Building prompt with context...")
    prompt = SYSTEM_PROMPT.format(context=context_string, question=question)

    # Step 4: Generate answer via LLM
    print(f"  [3/3] Generating answer with LLM...")
    answer = generate_answer(prompt)

    print(f"       ✓ Answer generated ({len(answer)} chars)")

    return RAGAnswer(
        question=question,
        answer=answer,
        citations=citations,
        context_string=context_string,
    )


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.chunker import Chunk
    from src.vectorstore import ingest_chunks, clear_vectorstore, get_vectorstore

    print("Testing chain module (end-to-end RAG)...\n")

    # Use a temporary DB for testing
    test_db = "./chroma_db_test"
    clear_vectorstore(db_path=test_db)

    # Ingest test chunks — a mini knowledge base about Python + SQL
    test_chunks = [
        Chunk("python_guide.pdf", 1,
              "Python is a high-level programming language created by Guido van Rossum in 1991. It emphasizes code readability and supports multiple programming paradigms.", 0),
        Chunk("python_guide.pdf", 2,
              "Lists in Python are ordered, mutable sequences that can hold mixed data types. Common operations include append(), extend(), insert(), and remove().", 0),
        Chunk("python_guide.pdf", 3,
              "Dictionaries in Python are key-value pairs. They are mutable and allow fast lookup by key. Creating a dict: my_dict = {'name': 'Alice', 'age': 30}.", 0),
        Chunk("sql_handbook.pdf", 1,
              "SQL (Structured Query Language) is used to manage relational databases. The SELECT statement retrieves data from one or more tables.", 0),
        Chunk("sql_handbook.pdf", 2,
              "JOINs in SQL combine rows from two or more tables based on a related column. INNER JOIN returns only matching rows; LEFT JOIN returns all rows from the left table.", 0),
        Chunk("sql_handbook.pdf", 3,
              "The WHERE clause in SQL filters rows based on conditions. Example: SELECT * FROM users WHERE age > 18 retrieves only adult users.", 0),
    ]
    print("Ingesting test knowledge base (6 chunks across 2 PDFs)...")
    ingest_chunks(test_chunks, db_path=test_db)

    # Test questions — one Python, one SQL, one out-of-scope
    test_questions = [
        "Who created Python?",
        "How do I join two tables in SQL?",
        "What is the capital of France?",  # out-of-scope — should say "I don't know"
    ]

    print("\n" + "=" * 70)
    for q in test_questions:
        print(f"\nQuestion: {q}")
        print("-" * 70)
        result = ask(q, db_path=test_db, top_k=3)
        print(f"\nAnswer: {result.answer}")
        print(f"\nCitations used:")
        for i, chunk in enumerate(result.citations, 1):
            print(f"  [{i}] {chunk.citation} (score: {chunk.score:.4f})")
        print("=" * 70)

    # Cleanup
    clear_vectorstore(db_path=test_db)
    print("\n✓ End-to-end RAG test complete.")