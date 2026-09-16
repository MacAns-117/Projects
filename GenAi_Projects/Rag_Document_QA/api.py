"""Optional FastAPI wrapper around the same pipeline.

    uvicorn api:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from src.chain import ask
from src.chunker import chunk_pages
from src.config import DEFAULT_DB_PATH, DEFAULT_TOP_K, MAX_PDFS, RETRIEVAL_METHODS
from src.pdf_loader import load_pdfs
from src.vectorstore import collection_count, ingest_chunks

app = FastAPI(title="RAG Document QA", version="1.1")


class IngestBody(BaseModel):
    paths: list[str] = Field(..., min_length=1, max_length=MAX_PDFS)


class AskBody(BaseModel):
    question: str
    top_k: int = DEFAULT_TOP_K
    method: str = "hybrid"


@app.get("/health")
def health():
    return {"ok": True, "chunks": collection_count(DEFAULT_DB_PATH)}


@app.post("/ingest")
def ingest(body: IngestBody):
    missing = [p for p in body.paths if not Path(p).exists()]
    if missing:
        raise HTTPException(400, f"missing files: {missing}")
    pages = load_pdfs(body.paths, verbose=False)
    chunks = chunk_pages(pages)
    n = ingest_chunks(chunks, db_path=DEFAULT_DB_PATH, replace_sources=True)
    return {"pages": len(pages), "chunks": n, "index": collection_count(DEFAULT_DB_PATH)}


@app.post("/ask")
def ask_route(body: AskBody):
    if body.method not in RETRIEVAL_METHODS:
        raise HTTPException(400, f"method must be one of {RETRIEVAL_METHODS}")
    if collection_count(DEFAULT_DB_PATH) == 0:
        raise HTTPException(409, "index is empty — POST /ingest first")
    result = ask(
        question=body.question,
        db_path=DEFAULT_DB_PATH,
        top_k=body.top_k,
        method=body.method,
    )
    return {
        "answer": result.answer,
        "method": result.method,
        "citations": [
            {"n": i, "citation": c.citation, "score": c.score}
            for i, c in enumerate(result.citations, 1)
        ],
    }
