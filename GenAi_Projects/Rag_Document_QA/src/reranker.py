"""Optional cross-encoder reranker. Lazy CPU load; fail open to no-rerank."""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING

from src.config import RERANKER_MODEL, RERANK_CANDIDATES

if TYPE_CHECKING:
    from src.retriever import RetrievedChunk

logger = logging.getLogger(__name__)

_model = None
_load_attempted = False
_load_failed = False


def rerank_env_preference() -> bool | None:
    """Return True/False if RAG_RERANK forces on/off, else None (auto)."""
    val = os.getenv("RAG_RERANK", "").strip().lower()
    if val in ("0", "false", "off", "no"):
        return False
    if val in ("1", "true", "on", "yes"):
        return True
    return None


def get_reranker(force: bool = False):
    """Load the cross-encoder once. Returns None if unavailable."""
    global _model, _load_attempted, _load_failed
    if _model is not None:
        return _model
    if _load_failed and not force:
        return None
    if _load_attempted and not force:
        return _model
    _load_attempted = True
    try:
        from sentence_transformers import CrossEncoder

        device = os.getenv("RAG_RERANKER_DEVICE", "cpu")
        _model = CrossEncoder(RERANKER_MODEL, device=device)
        _load_failed = False
        return _model
    except Exception as exc:  # noqa: BLE001 — fail open
        logger.warning("Reranker unavailable (%s); continuing without rerank.", exc)
        _load_failed = True
        _model = None
        return None


def reranker_available() -> bool:
    return get_reranker() is not None


def should_rerank(flag: bool | None = None) -> bool:
    """Resolve caller flag + env + model availability.

    - flag False → never
    - flag True → try (fail open if model missing)
    - flag None → env preference, else on only if model loads
    """
    pref = rerank_env_preference() if flag is None else flag
    if pref is False:
        return False
    if pref is True:
        return get_reranker() is not None
    # auto
    return get_reranker() is not None


def rerank_chunks(
    query: str,
    chunks: list["RetrievedChunk"],
    top_n: int,
    model=None,
) -> list["RetrievedChunk"]:
    """Re-score ``chunks`` with the cross-encoder and keep the top ``top_n``.

    On any failure, returns ``chunks[:top_n]`` unchanged (fail open).
    """
    if not chunks or top_n <= 0:
        return []
    if len(chunks) == 1:
        return chunks[:top_n]

    ce = model if model is not None else get_reranker()
    if ce is None:
        return chunks[:top_n]

    try:
        pairs = [(query, c.text) for c in chunks]
        scores = ce.predict(pairs)
        # numpy array or list
        scored = sorted(
            zip(chunks, scores),
            key=lambda x: float(x[1]),
            reverse=True,
        )
        out: list[RetrievedChunk] = []
        for chunk, score in scored[:top_n]:
            out.append(
                type(chunk)(
                    source=chunk.source,
                    page_num=chunk.page_num,
                    text=chunk.text,
                    score=float(score),
                    citation=chunk.citation,
                    method=f"{chunk.method}+rerank",
                )
            )
        return out
    except Exception as exc:  # noqa: BLE001
        logger.warning("Rerank failed (%s); using unreordered candidates.", exc)
        return chunks[:top_n]


def candidate_pool_size(top_k: int, configured: int = RERANK_CANDIDATES) -> int:
    """How many chunks to fetch before reranking."""
    return max(int(top_k), int(configured))
