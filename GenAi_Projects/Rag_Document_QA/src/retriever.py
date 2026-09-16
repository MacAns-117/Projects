"""
Retriever module — wraps Chroma's search with citation-friendly return types.

While vectorstore.similarity_search() returns raw Document objects, this
module returns RetrievedChunk objects that explicitly expose source,
page_num, text, and a citation string ready for display.

This centralizes the "extract citation info from metadata" logic so
downstream modules (chain.py, app.py) don't have to repeat it.
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_chroma import Chroma

from src.vectorstore import get_vectorstore, DEFAULT_TOP_K


@dataclass
class RetrievedChunk:
    """A chunk retrieved from the vector DB, with citation info exposed.

    Attributes:
        source: Filename of the original PDF (e.g., "resume.pdf").
        page_num: 1-indexed page number this chunk came from.
        text: The chunk text.
        score: Similarity score (0-1, higher = more similar). May be None
               if the underlying search didn't return scores.
        citation: A pre-formatted citation string like "resume.pdf, p.3".
    """
    source: str
    page_num: int
    text: str
    score: float | None
    citation: str


def _format_citation(source: str, page_num: int) -> str:
    """Format a citation string like 'resume.pdf, p.3'."""
    return f"{source}, p.{page_num}"


def _doc_to_retrieved(doc, score: float | None = None) -> RetrievedChunk:
    """Convert a LangChain Document to a RetrievedChunk.

    Extracts source and page from the document's metadata and formats
    a citation string. This is the single place where the metadata
    extraction logic lives — every consumer benefits.
    """
    metadata = doc.metadata or {}
    source = metadata.get("source", "unknown")
    page_num = metadata.get("page", 0)
    text = doc.page_content
    citation = _format_citation(source, page_num)
    return RetrievedChunk(
        source=source,
        page_num=page_num,
        text=text,
        score=score,
        citation=citation,
    )


def retrieve(
    query: str,
    vectorstore: Chroma | None = None,
    db_path: str | None = None,
    top_k: int = DEFAULT_TOP_K,
) -> list[RetrievedChunk]:
    """Retrieve the top-K most similar chunks for a query.

    Args:
        query: The user's question (natural language).
        vectorstore: An existing Chroma instance (optional — saves a
                     DB load if you already have one).
        db_path: Path to the persistent DB (used only if vectorstore
                 is None).
        top_k: Number of chunks to retrieve (default 4).

    Returns:
        List of RetrievedChunk objects, sorted by relevance (most
        similar first). Each chunk has source, page_num, text, score,
        and a pre-formatted citation string.

    Raises:
        ValueError: If neither vectorstore nor db_path is provided.
    """
    if vectorstore is None and db_path is None:
        raise ValueError("Must provide either vectorstore or db_path")

    if vectorstore is None:
        vectorstore = get_vectorstore(db_path=db_path)

    # similarity_search_with_score returns (Document, float) tuples
    # The score is a distance (lower = more similar) in Chroma's default mode
    raw_results = vectorstore.similarity_search_with_score(query, k=top_k)

    retrieved: list[RetrievedChunk] = []
    for doc, distance in raw_results:
        # Convert distance to similarity score (1 / (1 + distance))
        # This gives a 0-1 score where 1 = identical
        score = 1.0 / (1.0 + distance)
        retrieved.append(_doc_to_retrieved(doc, score=score))

    return retrieved


def retrieve_with_context(
    query: str,
    vectorstore: Chroma | None = None,
    db_path: str | None = None,
    top_k: int = DEFAULT_TOP_K,
) -> tuple[list[RetrievedChunk], str]:
    """Retrieve chunks AND format them as a context string for the LLM.

    The context string is what gets passed to the LLM as background
    information. It includes the chunk text and citation for each
    retrieved chunk, numbered for easy reference:

        [1] resume.pdf, p.3
        <chunk text>

        [2] report.pdf, p.7
        <chunk text>

    Args:
        Same as retrieve().

    Returns:
        Tuple of (retrieved_chunks, context_string).
    """
    chunks = retrieve(query, vectorstore, db_path, top_k)

    if not chunks:
        return [], "No relevant context found."

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        context_parts.append(f"[{i}] {chunk.citation}\n{chunk.text}")
    context_string = "\n\n".join(context_parts)

    return chunks, context_string


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.chunker import Chunk
    from src.vectorstore import ingest_chunks, clear_vectorstore

    print("Testing retriever module...\n")

    # Use a temporary DB for testing
    test_db = "./chroma_db_test"
    clear_vectorstore(db_path=test_db)

    # Ingest test chunks
    test_chunks = [
        Chunk("python_basics.pdf", 1,
              "Python is a high-level programming language known for its readable syntax.", 0),
        Chunk("python_basics.pdf", 2,
              "Lists in Python are ordered, mutable, and can hold mixed data types.", 0),
        Chunk("sql_basics.pdf", 1,
              "SQL is used to manage relational databases. SELECT retrieves data from tables.", 0),
        Chunk("sql_basics.pdf", 2,
              "JOINs combine rows from two or more tables based on a related column.", 0),
    ]
    ingest_chunks(test_chunks, db_path=test_db)

    # Test retrieve()
    print("\n--- retrieve() ---")
    query = "How do I join tables in SQL?"
    print(f"Query: {query}\n")
    results = retrieve(query, db_path=test_db, top_k=2)
    for i, chunk in enumerate(results, 1):
        print(f"  {i}. [{chunk.citation}] (score: {chunk.score:.4f})")
        preview = chunk.text[:100].replace("\n", " ")
        print(f"     {preview}...")

    # Test retrieve_with_context()
    print("\n--- retrieve_with_context() ---")
    chunks, context = retrieve_with_context(query, db_path=test_db, top_k=2)
    print("Context string for LLM:")
    print("-" * 60)
    print(context)
    print("-" * 60)

    # Cleanup
    clear_vectorstore(db_path=test_db)
    print("\n✓ Test complete.")