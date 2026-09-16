"""
Chunker module — splits page text into overlapping chunks for embedding.

Takes Page objects from pdf_loader and returns Chunk objects, each
carrying its source filename and page number as metadata. This
metadata is what lets the RAG system cite back to specific pages
later in the pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.pdf_loader import Page


@dataclass
class Chunk:
    """A single chunk of text extracted from a page.

    Attributes:
        source: Filename of the original PDF (e.g., "resume.pdf").
        page_num: 1-indexed page number this chunk came from.
        text: The chunk text (approx 1000 chars).
        chunk_index: Position of this chunk within the page (0, 1, 2, ...).
    """
    source: str
    page_num: int
    text: str
    chunk_index: int


# Default chunking parameters — tuned for general-purpose RAG
DEFAULT_CHUNK_SIZE = 1000      # characters per chunk
DEFAULT_CHUNK_OVERLAP = 200    # overlap between adjacent chunks (20%)


def _make_splitter(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> RecursiveCharacterTextSplitter:
    """Create a LangChain RecursiveCharacterTextSplitter.

    The "recursive" part means it tries to split on paragraph breaks
    first, then sentence breaks, then word breaks, then characters.
    This keeps chunks as natural-language units rather than arbitrary
    character counts.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # Split hierarchy: paragraphs > newlines > spaces > characters
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )


def chunk_page(
    page: Page,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Chunk]:
    """Split a single Page into chunks, preserving metadata.

    Args:
        page: A Page object from pdf_loader.
        chunk_size: Max characters per chunk (default 1000).
        chunk_overlap: Overlap between chunks (default 200).

    Returns:
        List of Chunk objects, each carrying the page's source and page_num.
    """
    splitter = _make_splitter(chunk_size, chunk_overlap)
    texts = splitter.split_text(page.text)

    chunks: list[Chunk] = []
    for i, text in enumerate(texts):
        chunks.append(
            Chunk(
                source=page.source,
                page_num=page.page_num,
                text=text,
                chunk_index=i,
            )
        )
    return chunks


def chunk_pages(
    pages: list[Page],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[Chunk]:
    """Split multiple pages into chunks.

    Args:
        pages: List of Page objects from pdf_loader.
        chunk_size: Max characters per chunk (default 1000).
        chunk_overlap: Overlap between chunks (default 200).

    Returns:
        List of Chunk objects from all pages, in order.
    """
    all_chunks: list[Chunk] = []
    for page in pages:
        page_chunks = chunk_page(page, chunk_size, chunk_overlap)
        all_chunks.extend(page_chunks)
        print(
            f"  ✓ {page.source} p.{page.page_num}: "
            f"{len(page_chunks)} chunks"
        )
    return all_chunks


# --- Quick self-test when run directly ---
if __name__ == "__main__":
    # Demo with synthetic data — no PDF needed
    sample_page = Page(
        source="demo.pdf",
        page_num=1,
        text=(
            "This is the first paragraph of a sample document. "
            "It contains enough text to demonstrate chunking behavior. "
            "The chunker will split this into smaller pieces.\n\n"
            "This is the second paragraph. It provides additional context. "
            "With a chunk size of 1000 characters, this entire demo text "
            "will likely fit in a single chunk, but real PDF pages (2000+ "
            "chars) will produce 2-3 chunks each.\n\n"
            "The overlap between chunks ensures that sentences spanning "
            "chunk boundaries are preserved in both chunks, so retrieval "
            "never loses context at the split point."
        ),
    )

    print(f"Input: {sample_page.source} p.{sample_page.page_num}")
    print(f"Text length: {len(sample_page.text)} chars\n")

    chunks = chunk_page(sample_page)
    print(f"\nOutput: {len(chunks)} chunks")
    for c in chunks:
        print(f"\n  Chunk {c.chunk_index} [{c.source} p.{c.page_num}]:")
        preview = c.text[:150].replace("\n", " ")
        print(f"    {preview}...")
        print(f"    Length: {len(c.text)} chars")