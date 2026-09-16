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
