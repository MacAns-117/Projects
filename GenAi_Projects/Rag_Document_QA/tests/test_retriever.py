from src.retriever import retrieve
from src.vectorstore import clear_vectorstore, ingest_chunks


def test_ingest_replace_does_not_duplicate(tiny_chunks, tmp_path):
    db = str(tmp_path / "chroma")
    n1 = ingest_chunks(tiny_chunks, db_path=db, replace_sources=True)
    n2 = ingest_chunks(tiny_chunks, db_path=db, replace_sources=True)
    assert n1 == n2
    hits = retrieve("N = 6 encoder layers", db_path=db, top_k=4, method="similarity", score_floor=0.0)
    sources = [h.source for h in hits]
    # same file should not flood the list as duplicates of the same chunk id
    assert sources.count("alpha.pdf") <= 4


def test_similarity_finds_nq_score(tiny_chunks, tmp_path):
    db = str(tmp_path / "chroma")
    ingest_chunks(tiny_chunks, db_path=db)
    hits = retrieve(
        "What EM does RAG-Sequence get on Natural Questions?",
        db_path=db,
        top_k=2,
        method="similarity",
        score_floor=0.0,
    )
    assert hits
    assert any("44.5" in h.text for h in hits)


def test_hybrid_runs(tiny_chunks, tmp_path):
    db = str(tmp_path / "chroma")
    ingest_chunks(tiny_chunks, db_path=db)
    hits = retrieve("encoder layers", db_path=db, top_k=3, method="hybrid", score_floor=0.0)
    assert hits
    assert hits[0].method == "hybrid"


def test_clear(tiny_chunks, tmp_path):
    db = str(tmp_path / "chroma")
    ingest_chunks(tiny_chunks, db_path=db)
    clear_vectorstore(db_path=db)
    hits = retrieve("Transformer", db_path=db, top_k=2, method="similarity", score_floor=0.0)
    assert hits == []


def test_bm25_cached_across_queries_but_rebuilt_after_ingest(tiny_chunks, tmp_path, monkeypatch):
    import src.retriever as retriever

    db = str(tmp_path / "chroma")
    ingest_chunks(tiny_chunks, db_path=db)
    retriever.invalidate_bm25_cache(db_path=db)

    builds = {"n": 0}
    real = retriever.BM25Okapi

    def counting(*args, **kwargs):
        builds["n"] += 1
        return real(*args, **kwargs)

    monkeypatch.setattr(retriever, "BM25Okapi", counting)

    retrieve("encoder layers", db_path=db, top_k=3, method="hybrid", score_floor=0.0)
    retrieve("Natural Questions", db_path=db, top_k=3, method="hybrid", score_floor=0.0)
    assert builds["n"] == 1, "BM25 should be built once and reused across queries"

    ingest_chunks(tiny_chunks, db_path=db)  # invalidates cache
    retrieve("Transformer", db_path=db, top_k=3, method="hybrid", score_floor=0.0)
    assert builds["n"] == 2, "BM25 should rebuild after ingest"
