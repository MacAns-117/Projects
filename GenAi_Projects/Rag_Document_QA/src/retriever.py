"""Three retrieval modes: cosine similarity, MMR, hybrid (vector + BM25)."""

from __future__ import annotations

from dataclasses import dataclass

from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi

from src.config import (
    DEFAULT_DB_PATH,
    DEFAULT_TOP_K,
    HYBRID_VECTOR_WEIGHT,
    MMR_LAMBDA,
    SCORE_FLOOR,
)
from src.vectorstore import get_vectorstore


@dataclass
class RetrievedChunk:
    source: str
    page_num: int
    text: str
    score: float | None
    citation: str
    method: str = "similarity"


def _citation(source: str, page_num: int) -> str:
    return f"{source}, p.{page_num}"


def _from_doc(doc, score: float | None, method: str) -> RetrievedChunk:
    meta = doc.metadata or {}
    source = str(meta.get("source", "unknown"))
    page_num = int(meta.get("page", 0))
    return RetrievedChunk(
        source=source,
        page_num=page_num,
        text=doc.page_content,
        score=score,
        citation=_citation(source, page_num),
        method=method,
    )


def _distance_to_sim(distance: float) -> float:
    return 1.0 / (1.0 + float(distance))


def _all_docs(vectorstore: Chroma, cap: int = 10_000) -> list:
    raw = vectorstore._collection.get(include=["documents", "metadatas"], limit=cap)
    from langchain_core.documents import Document

    docs = []
    for text, meta in zip(raw.get("documents") or [], raw.get("metadatas") or []):
        docs.append(Document(page_content=text or "", metadata=meta or {}))
    return docs


def retrieve_similarity(
    query: str,
    vectorstore: Chroma,
    top_k: int = DEFAULT_TOP_K,
    score_floor: float = SCORE_FLOOR,
) -> list[RetrievedChunk]:
    raw = vectorstore.similarity_search_with_score(query, k=top_k)
    out = []
    for doc, distance in raw:
        score = _distance_to_sim(distance)
        if score < score_floor:
            continue
        out.append(_from_doc(doc, score, "similarity"))
    return out


def retrieve_mmr(
    query: str,
    vectorstore: Chroma,
    top_k: int = DEFAULT_TOP_K,
    lambda_mult: float = MMR_LAMBDA,
    score_floor: float = SCORE_FLOOR,
) -> list[RetrievedChunk]:
    docs = vectorstore.max_marginal_relevance_search(
        query, k=top_k, fetch_k=max(top_k * 4, 16), lambda_mult=lambda_mult
    )
    # MMR API has no scores; approximate with a second similarity pass.
    scored = {
        (d.metadata.get("source"), d.metadata.get("page"), d.page_content[:80]): s
        for d, s in (
            (doc, _distance_to_sim(dist))
            for doc, dist in vectorstore.similarity_search_with_score(query, k=max(top_k * 4, 16))
        )
    }
    out = []
    for doc in docs:
        key = (doc.metadata.get("source"), doc.metadata.get("page"), doc.page_content[:80])
        score = scored.get(key)
        if score is not None and score < score_floor:
            continue
        out.append(_from_doc(doc, score, "mmr"))
    return out


def retrieve_hybrid(
    query: str,
    vectorstore: Chroma,
    top_k: int = DEFAULT_TOP_K,
    vector_weight: float = HYBRID_VECTOR_WEIGHT,
    score_floor: float = SCORE_FLOOR,
) -> list[RetrievedChunk]:
    docs = _all_docs(vectorstore)
    if not docs:
        return []

    tokenized = [d.page_content.lower().split() for d in docs]
    bm25 = BM25Okapi(tokenized)
    bm25_raw = bm25.get_scores(query.lower().split())
    bm25_max = max(float(x) for x in bm25_raw) or 1.0
    bm25_norm = [float(x) / bm25_max for x in bm25_raw]

    # Vector scores for a wider pool, then merge.
    vec_hits = vectorstore.similarity_search_with_score(query, k=min(len(docs), max(top_k * 8, 24)))
    vec_map: dict[tuple, float] = {}
    for doc, dist in vec_hits:
        key = (doc.metadata.get("source"), doc.metadata.get("page"), doc.page_content[:120])
        vec_map[key] = _distance_to_sim(dist)

    ranked: list[tuple[float, object]] = []
    for doc, bscore in zip(docs, bm25_norm):
        key = (doc.metadata.get("source"), doc.metadata.get("page"), doc.page_content[:120])
        vscore = vec_map.get(key, 0.0)
        combined = vector_weight * vscore + (1.0 - vector_weight) * bscore
        ranked.append((combined, doc))

    ranked.sort(key=lambda x: x[0], reverse=True)
    out = []
    for score, doc in ranked:
        if score < score_floor:
            continue
        out.append(_from_doc(doc, score, "hybrid"))
        if len(out) >= top_k:
            break
    return out


def retrieve(
    query: str,
    vectorstore: Chroma | None = None,
    db_path: str | None = None,
    top_k: int = DEFAULT_TOP_K,
    method: str = "hybrid",
    score_floor: float = SCORE_FLOOR,
) -> list[RetrievedChunk]:
    if vectorstore is None:
        if db_path is None:
            db_path = DEFAULT_DB_PATH
        from pathlib import Path

        if not Path(db_path).exists():
            return []
        vectorstore = get_vectorstore(db_path=db_path)

    method = (method or "hybrid").lower()
    if method == "mmr":
        return retrieve_mmr(vectorstore=vectorstore, query=query, top_k=top_k, score_floor=score_floor)
    if method == "similarity":
        return retrieve_similarity(
            vectorstore=vectorstore, query=query, top_k=top_k, score_floor=score_floor
        )
    return retrieve_hybrid(
        vectorstore=vectorstore, query=query, top_k=top_k, score_floor=score_floor
    )


def retrieve_with_context(
    query: str,
    vectorstore: Chroma | None = None,
    db_path: str | None = None,
    top_k: int = DEFAULT_TOP_K,
    method: str = "hybrid",
    score_floor: float = SCORE_FLOOR,
) -> tuple[list[RetrievedChunk], str]:
    chunks = retrieve(
        query,
        vectorstore=vectorstore,
        db_path=db_path,
        top_k=top_k,
        method=method,
        score_floor=score_floor,
    )
    if not chunks:
        return [], "No relevant context found."
    parts = [f"[{i}] {c.citation}\n{c.text}" for i, c in enumerate(chunks, 1)]
    return chunks, "\n\n".join(parts)
