"""Answer-quality eval (faithfulness / OOS refusal) via an OpenAI-compatible judge.

NOT run in CI and NOT run against paid APIs from this repo's automation.
Wire a local llama.cpp server or your own Groq key:

    export OPENAI_BASE_URL=http://127.0.0.1:8080/v1
    export OPENAI_API_KEY=local
    export JUDGE_MODEL=local-model
    python -m eval.run_faithfulness

Or with Groq:
    export GROQ_API_KEY=gsk_...
    export OPENAI_BASE_URL=https://api.groq.com/openai/v1
    export JUDGE_MODEL=openai/gpt-oss-120b
    python -m eval.run_faithfulness

By default this script refuses to start if no endpoint is configured, so a
bare `pytest` / CI run cannot accidentally bill anyone.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.faithfulness import grade_one, summarize
from eval.run_eval import build_eval_index, load_gold, resolve_pdf_dir
from src.chain import ask
from src.config import EVAL_DB_PATH, OPENAI_BASE_URL


def _endpoint_configured() -> bool:
    if OPENAI_BASE_URL or os.getenv("OPENAI_BASE_URL"):
        return True
    key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    return bool(key)


def main() -> None:
    if not _endpoint_configured():
        raise SystemExit(
            "Faithfulness eval needs OPENAI_BASE_URL (and usually OPENAI_API_KEY). "
            "See the docstring in eval/run_faithfulness.py. Not run without an endpoint."
        )

    gold = load_gold()
    pdf_dir, corpus = resolve_pdf_dir()
    n_chunks = build_eval_index(pdf_dir)
    print(f"indexed {n_chunks} chunks from {corpus}")

    results = []
    for q in gold["questions"]:
        # Retrieval + generation. OOS should refuse before the LLM when the gate fires.
        ans = ask(
            q["question"],
            db_path=EVAL_DB_PATH,
            method="hybrid",
            use_reranker=True,
        )
        graded = grade_one(
            question=q["question"],
            answer=ans.answer,
            context=ans.context_string,
            question_id=q["id"],
            out_of_scope=bool(q["out_of_scope"]),
        )
        results.append(graded)
        flag = "OK" if graded.grounded else "FAIL"
        print(f"[{flag}] {q['id']}: {graded.reason}")

    summary = summarize(results)
    ist = ZoneInfo("Asia/Calcutta")
    payload = {
        "run_at": datetime.now(tz=ist).isoformat(),
        "run_at_zone": "Asia/Calcutta",
        "corpus": corpus,
        "chunks": n_chunks,
        "summary": summary,
        "rows": [
            {
                "id": r.question_id,
                "grounded": r.grounded,
                "reason": r.reason,
                "out_of_scope": r.out_of_scope,
                "refused": r.refused,
                "answer": r.answer[:240],
            }
            for r in results
        ],
    }
    out = ROOT / "eval" / "faithfulness_results.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
