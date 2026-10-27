"""Retrieval eval over eval/gold_qa.json. No Groq key required.

Hit@k = at least one retrieved (source, page) matches a gold page.
MRR = mean reciprocal rank of the first gold page hit.
Out-of-scope items score as a 'refuse' retrieval hit when ZERO chunks remain
after the score floor + min-top-score gate.

Compares each method with and without the cross-encoder reranker.

Usage (from repo root):
    python -m eval.run_eval
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chunker import chunk_pages
from src.config import (
    ARXIV_PDF_DIR,
    DEFAULT_TOP_K,
    EVAL_DB_PATH,
    GOLD_QA_PATH,
    CE_MIN_SCORE,
    MIN_TOP_SCORE,
    RERANK_CANDIDATES,
    RERANKER_MODEL,
    RETRIEVAL_METHODS,
    SAMPLE_PDF_DIR,
    SCORE_FLOOR,
)
from src.pdf_loader import load_pdfs
from src.reranker import reranker_available
from src.retriever import retrieve
from src.vectorstore import clear_vectorstore, ingest_chunks


def load_gold() -> dict:
    return json.loads(GOLD_QA_PATH.read_text(encoding="utf-8"))


def resolve_pdf_dir() -> tuple[Path, str]:
    """Prefer full arXiv PDFs when present; else synthetic fixtures."""
    arxiv = sorted(ARXIV_PDF_DIR.glob("*.pdf")) if ARXIV_PDF_DIR.exists() else []
    if len(arxiv) >= 2:
        return ARXIV_PDF_DIR, "arxiv_full"
    sample = sorted(SAMPLE_PDF_DIR.glob("*.pdf"))
    if len(sample) >= 2:
        return SAMPLE_PDF_DIR, "synthetic_fixtures"
    raise SystemExit(
        f"Need PDFs in {ARXIV_PDF_DIR} (preferred) or {SAMPLE_PDF_DIR}. "
        "See data/README.md."
    )


def build_eval_index(pdf_dir: Path) -> int:
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if len(pdfs) < 2:
        raise SystemExit(f"Need two PDFs in {pdf_dir}")
    clear_vectorstore(db_path=EVAL_DB_PATH)
    pages = load_pdfs([str(p) for p in pdfs], verbose=True)
    chunks = chunk_pages(pages, verbose=False)
    n = ingest_chunks(chunks, db_path=EVAL_DB_PATH, replace_sources=True)
    return n


def page_hit(retrieved, gold_pages: list[dict]) -> bool:
    gold = {(g["source"], int(g["page"])) for g in gold_pages}
    got = {(c.source, int(c.page_num)) for c in retrieved}
    return bool(gold & got)


def reciprocal_rank(retrieved, gold_pages: list[dict]) -> float:
    gold = {(g["source"], int(g["page"])) for g in gold_pages}
    for i, c in enumerate(retrieved, 1):
        if (c.source, int(c.page_num)) in gold:
            return 1.0 / i
    return 0.0


def _run_method(
    questions: list[dict],
    method: str,
    top_k: int,
    use_reranker: bool,
) -> dict:
    hits = 0
    rr_sum = 0.0
    oos_ok = 0
    oos_n = 0
    in_n = 0
    per: list[dict] = []
    for q in questions:
        retrieved = retrieve(
            q["question"],
            db_path=EVAL_DB_PATH,
            top_k=top_k,
            method=method,
            use_reranker=use_reranker,
        )
        if q["out_of_scope"]:
            oos_n += 1
            ok = len(retrieved) == 0
            oos_ok += int(ok)
            per.append(
                {
                    "id": q["id"],
                    "hit": ok,
                    "out_of_scope": True,
                    "n_retrieved": len(retrieved),
                    "rr": 1.0 if ok else 0.0,
                }
            )
        else:
            in_n += 1
            ok = page_hit(retrieved, q["gold_pages"])
            rr = reciprocal_rank(retrieved, q["gold_pages"])
            hits += int(ok)
            rr_sum += rr
            per.append(
                {
                    "id": q["id"],
                    "hit": ok,
                    "out_of_scope": False,
                    "n_retrieved": len(retrieved),
                    "rr": round(rr, 4),
                    "pages": [c.citation for c in retrieved[:5]],
                }
            )
    return {
        "hit_at_k": round(hits / in_n, 4) if in_n else 0.0,
        "mrr": round(rr_sum / in_n, 4) if in_n else 0.0,
        "hits": hits,
        "in_scope": in_n,
        "oos_refuse_rate": round(oos_ok / oos_n, 4) if oos_n else 0.0,
        "oos_ok": oos_ok,
        "oos_n": oos_n,
        "use_reranker": use_reranker,
        "rows": per,
    }


def evaluate(top_k: int = DEFAULT_TOP_K) -> dict:
    gold = load_gold()
    questions = gold["questions"]
    pdf_dir, corpus = resolve_pdf_dir()
    n_chunks = build_eval_index(pdf_dir)
    rerank_ok = reranker_available()

    by_method: dict[str, dict] = {}
    for method in RETRIEVAL_METHODS:
        by_method[method] = _run_method(
            questions, method, top_k=top_k, use_reranker=False
        )
        key = f"{method}+rerank"
        if rerank_ok:
            by_method[key] = _run_method(
                questions, method, top_k=top_k, use_reranker=True
            )
        else:
            by_method[key] = {
                "hit_at_k": None,
                "mrr": None,
                "hits": None,
                "in_scope": sum(1 for q in questions if not q["out_of_scope"]),
                "oos_refuse_rate": None,
                "oos_ok": None,
                "oos_n": sum(1 for q in questions if q["out_of_scope"]),
                "use_reranker": True,
                "skipped": "reranker unavailable",
                "rows": [],
            }

    ist = ZoneInfo("Asia/Calcutta")
    now = datetime.now(tz=ist)
    payload = {
        "top_k": top_k,
        "chunks": n_chunks,
        "n_questions": len(questions),
        "corpus": corpus,
        "pdf_dir": str(pdf_dir),
        "score_floor": SCORE_FLOOR,
        "min_top_score": MIN_TOP_SCORE,
        "rerank_candidates": RERANK_CANDIDATES,
        "reranker_model": RERANKER_MODEL if rerank_ok else None,
        "reranker_available": rerank_ok,
        "run_at": now.isoformat(),
        "run_at_zone": "Asia/Calcutta",
        "setup": (
            f"corpus={corpus}; MiniLM embeddings; hybrid weight 0.6; "
            f"score_floor={SCORE_FLOOR}; min_top_score={MIN_TOP_SCORE}; ce_min_score={CE_MIN_SCORE}; "
            f"rerank={RERANKER_MODEL if rerank_ok else 'unavailable'} "
            f"candidates={RERANK_CANDIDATES}→{top_k}; device=cpu"
        ),
        "methods": {
            m: {k: v for k, v in d.items() if k != "rows"} for m, d in by_method.items()
        },
        "detail": {m: d.get("rows", []) for m, d in by_method.items()},
    }
    return payload


def write_outputs(payload: dict) -> None:
    out_json = ROOT / "eval" / "results.json"
    out_md = ROOT / "eval" / "results.md"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Retrieval eval",
        "",
        f"**Run:** {payload.get('run_at', '(unknown)')} ({payload.get('run_at_zone', '')})",
        "",
        f"Index: **{payload['chunks']}** chunks from `{payload.get('corpus')}` "
        f"(`{payload.get('pdf_dir')}`). top_k = **{payload['top_k']}**. "
        f"{payload['n_questions']} questions (22 in-scope, 2 out-of-scope).",
        "",
        f"Setup: `{payload.get('setup')}`",
        "",
        "Hit@k = at least one retrieved `(source, page)` is in the gold page list. "
        "MRR = mean reciprocal rank of the first gold-page hit (in-scope only). "
        "Out-of-scope “refuse” = retrieval returned **no** chunks after the score floor / "
        f"min_top_score={payload.get('min_top_score')} (no-rerank) and, when reranking, "
        "the cross-encoder logit floor (see config CE_MIN_SCORE).",
        "",
        "| Method | Hit@8 | MRR | Hits | OOS refuse | Rerank |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for method, stats in payload["methods"].items():
        if stats.get("hit_at_k") is None:
            lines.append(
                f"| `{method}` | — | — | — | — | skipped ({stats.get('skipped', '')}) |"
            )
            continue
        lines.append(
            f"| `{method}` | **{stats['hit_at_k']:.1%}** | "
            f"**{stats['mrr']:.3f}** | "
            f"{stats['hits']}/{stats['in_scope']} | "
            f"{stats['oos_ok']}/{stats['oos_n']} ({stats['oos_refuse_rate']:.0%}) | "
            f"{'yes' if stats.get('use_reranker') else 'no'} |"
        )
    lines += [
        "",
        "Hybrid is vector + BM25 on the same chunk list. MMR is Chroma’s "
        "`max_marginal_relevance_search`. Similarity is cosine on MiniLM. "
        "`*+rerank` re-scores the top "
        f"{payload.get('rerank_candidates', 20)} candidates with "
        f"`{payload.get('reranker_model') or '—'}` and keeps top_k.",
        "",
        "Generation faithfulness is a separate script: `python -m eval.run_faithfulness` "
        "(needs an OpenAI-compatible endpoint; not run in CI).",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        # Prefer hybrid / hybrid+rerank bars when present
        prefer = [m for m in ("similarity", "mmr", "hybrid", "hybrid+rerank") if m in payload["methods"]]
        methods = prefer or list(payload["methods"].keys())
        hits = []
        labels = []
        for m in methods:
            v = payload["methods"][m].get("hit_at_k")
            if v is None:
                continue
            labels.append(m)
            hits.append(v * 100)
        if labels:
            fig, ax = plt.subplots(figsize=(7.2, 3.6))
            colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2"]
            ax.bar(labels, hits, color=colors[: len(labels)])
            ax.set_ylim(0, 100)
            ax.set_ylabel(f"Hit@{payload['top_k']} (%)")
            ax.set_title("Retrieval hit-rate on 22 in-scope gold questions")
            for i, v in enumerate(hits):
                ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=9)
            fig.tight_layout()
            fig_path = ROOT / "eval" / "figures" / "hit_at_8.png"
            fig_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(fig_path, dpi=140)
            plt.close()
    except Exception as exc:
        print("figure skipped:", exc)


def main() -> None:
    payload = evaluate()
    write_outputs(payload)
    print(json.dumps(payload["methods"], indent=2))
    print("wrote eval/results.md")


if __name__ == "__main__":
    main()
