"""Retrieval eval over eval/gold_qa.json. No Groq key required.

Hit@k = at least one retrieved (source, page) matches a gold page.
Out-of-scope items score as a 'refuse' retrieval hit when ZERO in-scope
pages are retrieved (or the list is empty after the score floor).

Usage (from repo root):
    python -m eval.run_eval
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.chunker import chunk_pages
from src.config import (
    DEFAULT_TOP_K,
    EVAL_DB_PATH,
    GOLD_QA_PATH,
    RETRIEVAL_METHODS,
    SAMPLE_PDF_DIR,
)
from src.pdf_loader import load_pdfs
from src.retriever import retrieve
from src.vectorstore import clear_vectorstore, ingest_chunks


def load_gold() -> dict:
    return json.loads(GOLD_QA_PATH.read_text(encoding="utf-8"))


def build_eval_index() -> int:
    pdfs = sorted(SAMPLE_PDF_DIR.glob("*.pdf"))
    if len(pdfs) < 2:
        raise SystemExit(f"Need two sample PDFs in {SAMPLE_PDF_DIR}")
    clear_vectorstore(db_path=EVAL_DB_PATH)
    pages = load_pdfs([str(p) for p in pdfs], verbose=True)
    chunks = chunk_pages(pages, verbose=False)
    n = ingest_chunks(chunks, db_path=EVAL_DB_PATH, replace_sources=True)
    return n


def page_hit(retrieved, gold_pages: list[dict]) -> bool:
    gold = {(g["source"], int(g["page"])) for g in gold_pages}
    got = {(c.source, int(c.page_num)) for c in retrieved}
    return bool(gold & got)


def evaluate(top_k: int = DEFAULT_TOP_K) -> dict:
    gold = load_gold()
    questions = gold["questions"]
    n_chunks = build_eval_index()

    by_method: dict[str, dict] = {}
    for method in RETRIEVAL_METHODS:
        hits = 0
        oos_ok = 0
        oos_n = 0
        in_n = 0
        per: list[dict] = []
        for q in questions:
            retrieved = retrieve(
                q["question"], db_path=EVAL_DB_PATH, top_k=top_k, method=method
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
                    }
                )
            else:
                in_n += 1
                ok = page_hit(retrieved, q["gold_pages"])
                hits += int(ok)
                per.append(
                    {
                        "id": q["id"],
                        "hit": ok,
                        "out_of_scope": False,
                        "n_retrieved": len(retrieved),
                        "pages": [c.citation for c in retrieved[:5]],
                    }
                )
        by_method[method] = {
            "hit_at_k": round(hits / in_n, 4) if in_n else 0.0,
            "hits": hits,
            "in_scope": in_n,
            "oos_refuse_rate": round(oos_ok / oos_n, 4) if oos_n else 0.0,
            "oos_ok": oos_ok,
            "oos_n": oos_n,
            "rows": per,
        }

    payload = {
        "top_k": top_k,
        "chunks": n_chunks,
        "n_questions": len(questions),
        "methods": {m: {k: v for k, v in d.items() if k != "rows"} for m, d in by_method.items()},
        "detail": {m: d["rows"] for m, d in by_method.items()},
    }
    return payload


def write_outputs(payload: dict) -> None:
    out_json = ROOT / "eval" / "results.json"
    out_md = ROOT / "eval" / "results.md"
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Retrieval eval",
        "",
        f"Index: **{payload['chunks']}** chunks from the two sample arXiv PDFs. "
        f"top_k = **{payload['top_k']}**. "
        f"{payload['n_questions']} questions (22 in-scope, 2 out-of-scope).",
        "",
        "Hit@k = at least one retrieved `(source, page)` is in the gold page list. "
        "Out-of-scope “refuse” = retrieval returned **no** chunks after the score floor "
        "(the LLM is then forced to say it does not know).",
        "",
        "| Method | Hit@8 | Hits | OOS refuse |",
        "| --- | ---: | ---: | ---: |",
    ]
    for method, stats in payload["methods"].items():
        lines.append(
            f"| `{method}` | **{stats['hit_at_k']:.1%}** | "
            f"{stats['hits']}/{stats['in_scope']} | "
            f"{stats['oos_ok']}/{stats['oos_n']} ({stats['oos_refuse_rate']:.0%}) |"
        )
    lines += [
        "",
        "Hybrid is vector + BM25 on the same chunk list. MMR is Chroma’s "
        "`max_marginal_relevance_search`. Similarity is cosine on MiniLM.",
        "",
        "Generation (Groq) is **not** in this table — that path needs `GROQ_API_KEY` "
        "and is checked only in the live app / `ask()`.",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")

    # bar chart
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        methods = list(payload["methods"].keys())
        hits = [payload["methods"][m]["hit_at_k"] * 100 for m in methods]
        fig, ax = plt.subplots(figsize=(6.2, 3.4))
        ax.bar(methods, hits, color=["#4C78A8", "#F58518", "#54A24B"])
        ax.set_ylim(0, 100)
        ax.set_ylabel("Hit@8 (%)")
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
