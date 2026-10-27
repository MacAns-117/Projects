"""Answer-quality eval (faithfulness / OOS refusal) via an OpenAI-compatible judge.

NOT run in CI and NOT run against paid APIs from this repo's automation.
Generation and judging both reuse the app's LLM_* settings (src/llm.py).

Local llama.cpp / Ollama / LM Studio (free, nothing leaves your machine):

    export LLM_PROVIDER=openai_compatible
    export LLM_BASE_URL=http://localhost:8080/v1
    export LLM_MODEL=<model name your server serves>
    python -m eval.run_faithfulness

Or with your own Groq key (default provider):
    export GROQ_API_KEY=gsk_...
    python -m eval.run_faithfulness

Judge-only override (e.g. generate locally, judge elsewhere):
    export OPENAI_BASE_URL=... OPENAI_API_KEY=... JUDGE_MODEL=...

By default this script refuses to start if no endpoint is configured, so a
bare `pytest` / CI run cannot accidentally bill anyone.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eval.faithfulness import grade_one, resolve_judge_settings, summarize
from eval.run_eval import build_eval_index, load_gold, resolve_pdf_dir
from src.chain import ask
from src.config import EVAL_DB_PATH
from src.llm import llm_label, validate as validate_llm


def main() -> None:
    try:
        judge = resolve_judge_settings()
        validate_llm()  # generation side
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(
            f"{exc}\nSee the docstring in eval/run_faithfulness.py. "
            "Not run without an endpoint."
        )
    print(f"generator: {llm_label()}")
    print(f"judge: {judge.model} @ {judge.base_url}")

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
        "generator": llm_label(),
        "judge": {"model": judge.model, "base_url": judge.base_url},
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
