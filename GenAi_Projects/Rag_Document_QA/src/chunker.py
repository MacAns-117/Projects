"""Split pages into overlapping chunks. Metadata (source, page) stays on every chunk."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.pdf_loader import Page


@dataclass
class Chunk:
    source: str
    page_num: int
    text: str
    chunk_index: int


def _splitter(chunk_size: int, chunk_overlap: int) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
    )


def chunk_page(
    page: Page,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    texts = _splitter(chunk_size, chunk_overlap).split_text(page.text)
    return [
        Chunk(
            source=page.source,
            page_num=page.page_num,
            text=text,
            chunk_index=i,
        )
        for i, text in enumerate(texts)
    ]


def chunk_pages(
    pages: list[Page],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    verbose: bool = False,
) -> list[Chunk]:
    out: list[Chunk] = []
    for page in pages:
        page_chunks = chunk_page(page, chunk_size, chunk_overlap)
        out.extend(page_chunks)
        if verbose:
            print(f"  {page.source} p.{page.page_num}: {len(page_chunks)} chunks")
    return out


def chunk_id(chunk: Chunk) -> str:
    """Stable id so re-ingest of the same file overwrites instead of duplicating."""
    safe = chunk.source.replace("/", "_")
    return f"{safe}::p{chunk.page_num}::c{chunk.chunk_index}"
