"""Out-of-scope questions must yield empty retrieval / refusal, not random chunks."""

from __future__ import annotations

from src.chain import REFUSAL, ask
from src.retriever import RetrievedChunk, apply_ce_min_score, apply_min_top_score, retrieve
from src.vectorstore import ingest_chunks


def test_apply_min_top_score_drops_weak_hits():
    chunks = [
        RetrievedChunk("a.pdf", 1, "hello", 0.25, "a.pdf, p.1", "hybrid"),
        RetrievedChunk("a.pdf", 2, "world", 0.20, "a.pdf, p.2", "hybrid"),
    ]
    assert apply_min_top_score(chunks, min_top_score=0.32) == []
    assert apply_min_top_score(chunks, min_top_score=0.20) == chunks


def test_apply_ce_min_score_refuses_negative_logits():
    chunks = [
        RetrievedChunk("a.pdf", 1, "hello", -11.0, "a.pdf, p.1", "hybrid+rerank"),
        RetrievedChunk("a.pdf", 2, "world", -10.5, "a.pdf, p.2", "hybrid+rerank"),
    ]
    assert apply_ce_min_score(chunks, ce_min_score=-9.0) == []
    ok = [
        RetrievedChunk("a.pdf", 1, "layers", 8.5, "a.pdf, p.1", "hybrid+rerank"),
    ]
    assert apply_ce_min_score(ok, ce_min_score=-9.0) == ok


def test_oos_question_empty_with_reranker_gate(tiny_chunks, tmp_path):
    """CE logits for geography/people vs paper chunks are ~-11 → refuse."""
    db = str(tmp_path / "chroma")
    ingest_chunks(tiny_chunks, db_path=db)
    hits = retrieve(
        "What is the capital of France?",
        db_path=db,
        top_k=8,
        method="hybrid",
        use_reranker=True,
        ce_min_score=-9.0,
        score_floor=0.0,
        min_top_score=0.0,
    )
    assert hits == []


def test_ask_refuses_oos_without_calling_llm(tiny_chunks, tmp_path, monkeypatch):
    db = str(tmp_path / "chroma")
    ingest_chunks(tiny_chunks, db_path=db)

    def boom(*a, **k):
        raise AssertionError("LLM should not be called on empty retrieval")

    monkeypatch.setattr("src.llm.generate_answer", boom)

    result = ask(
        "Who was the software engineer at Aptsol in 2024?",
        db_path=db,
        method="hybrid",
        use_reranker=True,
        ce_min_score=-9.0,
    )
    assert result.answer == REFUSAL
    assert result.citations == []
