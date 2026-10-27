"""Three retrieval modes: cosine similarity, MMR, hybrid (vector + BM25), optional rerank."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi

from src.config import (
    CE_MIN_SCORE,
    DEFAULT_COLLECTION,
    DEFAULT_DB_PATH,
    DEFAULT_TOP_K,
    HYBRID_VECTOR_WEIGHT,
    MIN_TOP_SCORE,
    MMR_LAMBDA,
    SCORE_FLOOR,
)
from src.vectorstore import get_vectorstore

# BM25 is built from the full collection — cache it and invalidate on ingest/clear.
_bm25_cache: dict[str, dict] = {}


def _cache_key(vectorstore: Chroma, db_path: str | None = None) -> str:
    persist = db_path or getattr(vectorstore, "_persist_directory", None) or ""
    try:
        persist = str(Path(persist).resolve()) if persist else ""
    except OSError:
        persist = str(persist)
    try:
        coll = vectorstore._collection.name
    except Exception:
        coll = DEFAULT_COLLECTION
    return f"{persist}::{coll}"


def invalidate_bm25_cache(
    db_path: str | None = None,
    collection_name: str | None = None,
) -> None:
    """Drop cached BM25 indexes. Call after ingest or clear."""
    if db_path is None:
        _bm25_cache.clear()
        return
    try:
        prefix = str(Path(db_path).resolve())
    except OSError:
        prefix = str(db_path)
    coll = collection_name or DEFAULT_COLLECTION
    exact = f"{prefix}::{coll}"
    _bm25_cache.pop(exact, None)
    for key in list(_bm25_cache):
        if key.startswith(prefix + "::"):
            _bm25_cache.pop(key, None)


def _get_bm25_index(
    vectorstore: Chroma,
    db_path: str | None = None,
) -> tuple[BM25Okapi | None, list]:
    """Return (bm25, docs), building once per collection until invalidated."""
    key = _cache_key(vectorstore, db_path=db_path)
    cached = _bm25_cache.get(key)
    if cached is not None:
        return cached["bm25"], cached["docs"]

    docs = _all_docs(vectorstore)
    if not docs:
        bm25 = None
    else:
        tokenized = [d.page_content.lower().split() for d in docs]
        bm25 = BM25Okapi(tokenized)
    _bm25_cache[key] = {"bm25": bm25, "docs": docs}
    return bm25, docs


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


def apply_min_top_score(
    chunks: list[RetrievedChunk],
    min_top_score: float | None = MIN_TOP_SCORE,
) -> list[RetrievedChunk]:
    """Drop the whole result set when the best *retrieval* score is below the gate.

    Only applies to non-negative scores (hybrid / similarity). Cross-encoder
    logits use ``apply_ce_min_score`` instead.
    """
    if not chunks or min_top_score is None or min_top_score <= 0:
        return chunks
    scored = [c.score for c in chunks if c.score is not None]
    if not scored:
        return chunks
    if any(s < 0 for s in scored):
        return chunks
    if max(scored) < min_top_score:
        return []
    return chunks


def apply_ce_min_score(
    chunks: list[RetrievedChunk],
    ce_min_score: float | None = CE_MIN_SCORE,
) -> list[RetrievedChunk]:
    """After cross-encoder rerank: refuse if the best logit is below ``ce_min_score``.

    ms-marco-MiniLM scores in-scope hits well above 0 and OOS queries around -10.
    """
    if not chunks or ce_min_score is None:
        return chunks
    scored = [c.score for c in chunks if c.score is not None]
    if not scored:
        return chunks
    if max(scored) < ce_min_score:
        return []
    return chunks


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
    scored = {
        (d.metadata.get("source"), d.metadata.get("page"), d.page_content[:80]): s
        for d, s in (
            (doc, _distance_to_sim(dist))
            for doc, dist in vectorstore.similarity_search_with_score(
                query, k=max(top_k * 4, 16)
            )
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
    db_path: str | None = None,
) -> list[RetrievedChunk]:
    bm25, docs = _get_bm25_index(vectorstore, db_path=db_path)
    if not docs or bm25 is None:
        return []

    bm25_raw = bm25.get_scores(query.lower().split())
    bm25_max = max(float(x) for x in bm25_raw) or 1.0
    bm25_norm = [float(x) / bm25_max for x in bm25_raw]

    vec_hits = vectorstore.similarity_search_with_score(
        query, k=min(len(docs), max(top_k * 8, 24))
    )
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
    use_reranker: bool | None = None,
    min_top_score: float | None = MIN_TOP_SCORE,
    ce_min_score: float | None = CE_MIN_SCORE,
) -> list[RetrievedChunk]:
    resolved_path = db_path
    if vectorstore is None:
        if db_path is None:
            db_path = DEFAULT_DB_PATH
        resolved_path = db_path

        if not Path(db_path).exists():
            return []
        vectorstore = get_vectorstore(db_path=db_path)

    from src.reranker import candidate_pool_size, rerank_chunks, should_rerank

    do_rerank = should_rerank(use_reranker)
    fetch_k = candidate_pool_size(top_k) if do_rerank else top_k

    method = (method or "hybrid").lower()
    if method == "mmr":
        chunks = retrieve_mmr(
            vectorstore=vectorstore, query=query, top_k=fetch_k, score_floor=score_floor
        )
    elif method == "similarity":
        chunks = retrieve_similarity(
            vectorstore=vectorstore, query=query, top_k=fetch_k, score_floor=score_floor
        )
    else:
        chunks = retrieve_hybrid(
            vectorstore=vectorstore,
            query=query,
            top_k=fetch_k,
            score_floor=score_floor,
            db_path=resolved_path,
        )

    if do_rerank:
        # Rerank first, then CE logit gate (primary OOS refusal when model loads).
        chunks = rerank_chunks(query, chunks, top_n=max(top_k, len(chunks)))
        chunks = apply_ce_min_score(chunks, ce_min_score=ce_min_score)
        return chunks[:top_k]

    # No reranker: keep retrieval-score OOS gate, then trim.
    chunks = apply_min_top_score(chunks, min_top_score=min_top_score)
    return chunks[:top_k]


def retrieve_with_context(
    query: str,
    vectorstore: Chroma | None = None,
    db_path: str | None = None,
    top_k: int = DEFAULT_TOP_K,
    method: str = "hybrid",
    score_floor: float = SCORE_FLOOR,
    use_reranker: bool | None = None,
    min_top_score: float | None = MIN_TOP_SCORE,
    ce_min_score: float | None = CE_MIN_SCORE,
) -> tuple[list[RetrievedChunk], str]:
    chunks = retrieve(
        query,
        vectorstore=vectorstore,
        db_path=db_path,
        top_k=top_k,
        method=method,
        score_floor=score_floor,
        use_reranker=use_reranker,
        min_top_score=min_top_score,
        ce_min_score=ce_min_score,
    )
    if not chunks:
        return [], "No relevant context found."
    parts = [f"[{i}] {c.citation}\n{c.text}" for i, c in enumerate(chunks, 1)]
    return chunks, "\n\n".join(parts)
