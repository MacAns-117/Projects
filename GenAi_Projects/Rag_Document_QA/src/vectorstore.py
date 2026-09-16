"""
Vectorstore module — persistent Chroma vector database for storing
and searching embedded text chunks.

When you ingest chunks, they get embedded (via embeddings.py) and
saved to disk. When you search later, Chroma finds the most similar
chunks to a query using cosine similarity.

The database persists in ./chroma_db/ — survives restarts, so you
only ingest PDFs once. Subsequent app starts load the existing DB
instantly.
"""




from __future__ import annotations

import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_DISABLED"] = "1"

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.chunker import Chunk
from src.embeddings import get_embeddings


# Default location for the persistent vector database
# This path is relative to the project root (Rag_Document_QA folder)
DEFAULT_DB_PATH = "./chroma_db"

# Default collection name inside Chroma
# A single Chroma DB can hold multiple named collections
DEFAULT_COLLECTION = "pdf_chunks"

# Default number of chunks to retrieve per query
DEFAULT_TOP_K = 8


def get_vectorstore(
    db_path: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embeddings: Embeddings | None = None,
) -> Chroma:
    """Get a Chroma vectorstore instance.

    Loads an existing persistent DB if one exists at db_path, or
    creates a new empty one if not. The embeddings model is used
    both for ingesting chunks (convert text → vector) and for
    searching (convert query → vector → compare).

    Args:
        db_path: Path to the persistent Chroma database directory.
        collection_name: Name of the collection inside the DB.
        embeddings: Embeddings instance (defaults to the cached
                    HuggingFace model from embeddings.py).

    Returns:
        Chroma vectorstore instance.
    """
    if embeddings is None:
        embeddings = get_embeddings()

    # Ensure the DB directory exists (Chroma won't create it automatically)
    Path(db_path).mkdir(parents=True, exist_ok=True)

    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_path,
    )


def ingest_chunks(
    chunks: list[Chunk],
    db_path: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embeddings: Embeddings | None = None,
) -> int:
    """Embed and store chunks in the persistent vector DB.

    Each chunk is stored as a Chroma Document with:
      - page_content: the chunk text
      - metadata: source filename, page number, chunk index

    This metadata is what lets the retriever cite back to specific
    pages later. Without it, the system could only return the
    matching text — not WHERE it came from.

    Args:
        chunks: List of Chunk objects (from chunker.py).
        db_path: Path to the persistent Chroma database.
        collection_name: Name of the collection inside the DB.
        embeddings: Embeddings instance (defaults to cached model).

    Returns:
        Number of chunks successfully ingested.
    """
    if not chunks:
        print("  ⚠ No chunks to ingest")
        return 0

    vectorstore = get_vectorstore(db_path, collection_name, embeddings)

    # Convert our Chunk objects to LangChain Document objects
    documents: list[Document] = []
    for chunk in chunks:
        doc = Document(
            page_content=chunk.text,
            metadata={
                "source": chunk.source,
                "page": chunk.page_num,
                "chunk_index": chunk.chunk_index,
            },
        )
        documents.append(doc)

    # Batch insert — Chroma handles the embedding internally
    vectorstore.add_documents(documents)

    print(
        f"  ✓ Ingested {len(documents)} chunks "
        f"({len(set(c.source for c in chunks))} files) "
        f"→ {db_path}"
    )
    return len(documents)


def clear_vectorstore(
    db_path: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embeddings: Embeddings | None = None,
) -> None:
    """Delete all chunks from the vector DB.

    Useful when you want to re-ingest PDFs from scratch (e.g., after
    changing chunk_size or embedding model). This deletes the
    collection's contents but keeps the DB directory.
    """
    import shutil

    vectorstore = get_vectorstore(db_path, collection_name, embeddings)
    vectorstore.delete_collection()

    # Optionally remove the entire DB directory if it's now empty
    db_dir = Path(db_path)
    if db_dir.exists() and not any(db_dir.iterdir()):
        db_dir.rmdir()

    print(f"  ✓ Cleared vector DB at {db_path}")


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    from src.chunker import Chunk

    print("Testing vectorstore module...\n")

    # Create test chunks (synthetic — no PDF needed)
    test_chunks = [
        Chunk(
            source="python_basics.pdf",
            page_num=1,
            text="Python is a high-level programming language known for its readable syntax and large standard library. It supports multiple paradigms including procedural, object-oriented, and functional programming.",
            chunk_index=0,
        ),
        Chunk(
            source="python_basics.pdf",
            page_num=2,
            text="Lists in Python are ordered, mutable, and can hold mixed data types. Common operations include append, extend, insert, remove, and sort. List comprehensions provide a concise way to create lists.",
            chunk_index=0,
        ),
        Chunk(
            source="sql_basics.pdf",
            page_num=1,
            text="SQL (Structured Query Language) is used to manage relational databases. The SELECT statement retrieves data from one or more tables. WHERE clauses filter rows based on conditions.",
            chunk_index=0,
        ),
        Chunk(
            source="sql_basics.pdf",
            page_num=2,
            text="JOINs combine rows from two or more tables based on a related column. INNER JOIN returns only matching rows. LEFT JOIN returns all rows from the left table plus matches from the right.",
            chunk_index=0,
        ),
    ]

    # Use a temporary DB path for testing
    test_db = "./chroma_db_test"

    # Clean up any leftover test DB from a previous run
    clear_vectorstore(db_path=test_db)

    # Ingest the test chunks
    print("\nIngesting test chunks...")
    count = ingest_chunks(test_chunks, db_path=test_db)
    print(f"Ingested {count} chunks\n")

    # Search the vector DB
    print("Searching for 'How do I join tables in SQL?'...")
    vectorstore = get_vectorstore(db_path=test_db)
    results = vectorstore.similarity_search(
        query="How do I join tables in SQL?",
        k=2,
    )

    print(f"\nTop {len(results)} results:")
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "?")
        page = doc.metadata.get("page", "?")
        preview = doc.page_content[:120].replace("\n", " ")
        print(f"  {i}. [{source} p.{page}]")
        print(f"     {preview}...")

    # Clean up the test DB
    print("\nCleaning up test DB...")
    clear_vectorstore(db_path=test_db)
    print("\n✓ Test complete.")