"""Persistent Chroma. Re-ingest of the same filename replaces those rows, it does not append."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
os.environ.setdefault("CHROMA_TELEMETRY_DISABLED", "1")

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.chunker import Chunk, chunk_id
from src.config import DEFAULT_COLLECTION, DEFAULT_DB_PATH
from src.embeddings import get_embeddings


def get_vectorstore(
    db_path: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embeddings: Embeddings | None = None,
) -> Chroma:
    if embeddings is None:
        embeddings = get_embeddings()
    Path(db_path).mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_path,
    )


def _delete_sources(vectorstore: Chroma, sources: set[str]) -> None:
    collection = vectorstore._collection
    for source in sources:
        try:
            collection.delete(where={"source": source})
        except Exception:
            pass


def ingest_chunks(
    chunks: list[Chunk],
    db_path: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embeddings: Embeddings | None = None,
    replace_sources: bool = True,
) -> int:
    if not chunks:
        return 0

    vectorstore = get_vectorstore(db_path, collection_name, embeddings)
    sources = {c.source for c in chunks}
    if replace_sources:
        _delete_sources(vectorstore, sources)

    documents: list[Document] = []
    ids: list[str] = []
    seen: set[str] = set()
    for chunk in chunks:
        cid = chunk_id(chunk)
        if cid in seen:
            continue
        seen.add(cid)
        ids.append(cid)
        documents.append(
            Document(
                page_content=chunk.text,
                metadata={
                    "source": chunk.source,
                    "page": int(chunk.page_num),
                    "chunk_index": int(chunk.chunk_index),
                },
            )
        )

    vectorstore.add_documents(documents, ids=ids)
    return len(documents)


def clear_vectorstore(
    db_path: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION,
    embeddings: Embeddings | None = None,
) -> None:
    import shutil

    db_dir = Path(db_path)
    if db_dir.exists():
        shutil.rmtree(db_dir, ignore_errors=True)


def collection_count(
    db_path: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION,
) -> int:
    try:
        vs = get_vectorstore(db_path, collection_name)
        return vs._collection.count()
    except Exception:
        return 0
