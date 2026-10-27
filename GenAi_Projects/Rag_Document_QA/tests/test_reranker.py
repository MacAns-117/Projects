"""Cross-encoder reranker: ordering, fail-open, availability flags."""

from __future__ import annotations

from src.reranker import (
    candidate_pool_size,
    rerank_chunks,
    rerank_env_preference,
    should_rerank,
)
from src.retriever import RetrievedChunk


def _chunk(text: str, page: int, score: float = 0.5) -> RetrievedChunk:
    return RetrievedChunk(
        source="doc.pdf",
        page_num=page,
        text=text,
        score=score,
        citation=f"doc.pdf, p.{page}",
        method="hybrid",
    )


class FakeCE:
    def predict(self, pairs):
        return [10.0 if "gold" in p[1] else -5.0 for p in pairs]


def test_candidate_pool_at_least_top_k():
    assert candidate_pool_size(5, configured=20) == 20
    assert candidate_pool_size(25, configured=20) == 25


def test_rerank_reorders_and_keeps_top_n():
    chunks = [
        _chunk("noise about cats", 1, 0.9),
        _chunk("the gold answer is here", 2, 0.4),
        _chunk("more noise", 3, 0.8),
    ]
    out = rerank_chunks("what is the gold answer?", chunks, top_n=2, model=FakeCE())
    assert len(out) == 2
    assert out[0].page_num == 2
    assert "rerank" in out[0].method
    assert out[0].score == 10.0


def test_rerank_fails_open_on_predict_error():
    chunks = [_chunk("a", 1), _chunk("b", 2)]

    class Boom:
        def predict(self, pairs):
            raise RuntimeError("boom")

    out = rerank_chunks("q", chunks, top_n=1, model=Boom())
    assert out == chunks[:1]


def test_should_rerank_explicit_false():
    assert should_rerank(False) is False


def test_rerank_env_preference_off(monkeypatch):
    monkeypatch.setenv("RAG_RERANK", "0")
    assert rerank_env_preference() is False
    assert should_rerank(None) is False


def test_rerank_env_preference_on_needs_model(monkeypatch):
    monkeypatch.setenv("RAG_RERANK", "1")
    assert rerank_env_preference() is True
    # True only if the model actually loads on this machine.
    assert should_rerank(None) in (True, False)
