"""Fact eval on the default hotel CSV (no LLM). Optional --llm for router/answer checks.

    python -m eval.run_eval
    python -m eval.run_eval --llm
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from src.data_loader import load_default

EVAL_DIR = Path(__file__).resolve().parent
GOLD_FILE = EVAL_DIR / "gold_questions.json"
RESULTS_JSON = EVAL_DIR / "results.json"
RESULTS_MD = EVAL_DIR / "results.md"


def load_gold() -> list[dict]:
    return json.loads(GOLD_FILE.read_text())


def _close(a, b, tol=0.05) -> bool:
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def pandas_facts(df) -> dict:
    cancel = df["is_canceled"].mean() * 100
    by_hotel = (df.groupby("hotel")["is_canceled"].mean() * 100).round(2).to_dict()
    lead_c = df.loc[df["is_canceled"] == 1, "lead_time"].mean()
    lead_n = df.loc[df["is_canceled"] == 0, "lead_time"].mean()
    adr_h = df.groupby("hotel")["adr"].mean().round(2).to_dict()
    months = df["arrival_date_month"].value_counts().to_dict()
    return {
        "row_count": len(df),
        "cancel_rate": round(cancel, 2),
        "cancel_by_hotel": by_hotel,
        "lead_by_cancel": {
            "canceled": round(lead_c, 1),
            "not_canceled": round(lead_n, 1),
        },
        "month_top": {"August": int(months.get("August", 0))},
        "adr_by_hotel": adr_h,
        "top_market": list(df["market_segment"].value_counts().head(3).index),
        "corr_lead_cancel": round(float(df["lead_time"].corr(df["is_canceled"])), 4),
        "top_countries": list(df["country"].value_counts().head(5).index),
        "special_cancel": {
            str(k): round(v * 100, 1)
            for k, v in df.groupby("total_of_special_requests")["is_canceled"].mean().items()
            if k in (0, 1)
        },
        "repeat_cancel": {
            str(k): round(v * 100, 2)
            for k, v in df.groupby("is_repeated_guest")["is_canceled"].mean().items()
        },
        "years": {str(k): int(v) for k, v in df["arrival_date_year"].value_counts().sort_index().items()},
        "booking_changes_mean": round(float(df["booking_changes"].mean()), 3),
        "deposit_cancel": {
            str(k): round(v * 100, 2)
            for k, v in df.groupby("deposit_type")["is_canceled"].mean().items()
        },
        "nights": {
            "weekend": round(float(df["stays_in_weekend_nights"].mean()), 3),
            "week": round(float(df["stays_in_week_nights"].mean()), 3),
        },
        "families": int(((df["children"].fillna(0) + df["babies"].fillna(0)) > 0).sum()),
        "wait_mean": round(float(df["days_in_waiting_list"].mean()), 3),
        "adr_by_customer": df.groupby("customer_type")["adr"].mean().round(2).to_dict(),
        "busiest_month": df["arrival_date_month"].value_counts().idxmax(),
    }


def check_fact(check: str | None, expected, facts: dict) -> bool | None:
    if not check:
        return None
    got = facts.get(check)
    if isinstance(expected, dict) and isinstance(got, dict):
        return all(_close(got.get(k), v, tol=0.15) or got.get(k) == v for k, v in expected.items())
    if isinstance(expected, list):
        return list(got)[: len(expected)] == expected
    if isinstance(expected, (int, float)):
        return _close(got, expected, tol=0.05 if isinstance(expected, float) else 0)
    return got == expected


def phrase_hit(answer: str, phrases: list[str]) -> bool:
    low = answer.lower()
    return any(p.lower() in low for p in phrases)


def run_pandas_eval(df, gold: list[dict]) -> dict:
    facts = pandas_facts(df)
    rows = []
    n_ok = 0
    n_checked = 0
    for q in gold:
        ok = check_fact(q.get("check"), q.get("expected"), facts)
        if ok is None:
            rows.append({"id": q["id"], "pandas_ok": None, "note": "no numeric check"})
            continue
        n_checked += 1
        n_ok += int(bool(ok))
        rows.append({"id": q["id"], "pandas_ok": bool(ok)})
    return {
        "facts": facts,
        "rows": rows,
        "pandas_pass": n_ok,
        "pandas_checked": n_checked,
    }


def run_llm_eval(df, gold: list[dict]) -> list[dict]:
    from src.orchestrator import create_orchestrator, empty_state

    orch = create_orchestrator(df)
    out = []
    for q in gold:
        start = time.time()
        try:
            state = orch.invoke(empty_state(q["question"]))
            answer = state.get("final_answer") or ""
            intent_ok = state.get("intent") == q["intent"]
            ans_ok = phrase_hit(answer, q.get("answer_contains") or [])
            out.append(
                {
                    "id": q["id"],
                    "intent_ok": intent_ok,
                    "answer_ok": ans_ok,
                    "actual_intent": state.get("intent"),
                    "elapsed_sec": round(time.time() - start, 1),
                    "answer_preview": answer[:220],
                    "has_chart": state.get("chart_fig") is not None,
                }
            )
        except Exception as exc:
            out.append({"id": q["id"], "error": str(exc), "intent_ok": False, "answer_ok": False})
    return out


def write_outputs(payload: dict) -> None:
    RESULTS_JSON.write_text(json.dumps(payload, indent=2, default=str))
    s = payload["summary"]
    lines = [
        "# CSV Insights — eval",
        "",
        "Default table: hotel bookings after clean (arrivals July 2015 – August 2017).",
        "",
        "## Pandas facts (no LLM)",
        "",
        f"- Checks passed: **{s['pandas_pass']}/{s['pandas_checked']}**",
        f"- Clean rows: **{s['row_count']:,}**",
        f"- Cancellation rate: **{s['cancel_rate']}%**",
        f"- Lead time canceled vs stayed: **{s['lead_canceled']} vs {s['lead_stayed']} days**",
        f"- Busiest arrival month: **{s['busiest_month']}**",
        "",
        "| id | pandas |",
        "|---|---|",
    ]
    for r in payload["pandas_rows"]:
        mark = "—" if r["pandas_ok"] is None else ("pass" if r["pandas_ok"] else "fail")
        lines.append(f"| {r['id']} | {mark} |")
    if payload.get("llm_rows"):
        intent_n = sum(1 for r in payload["llm_rows"] if r.get("intent_ok"))
        ans_n = sum(1 for r in payload["llm_rows"] if r.get("answer_ok"))
        total = len(payload["llm_rows"])
        lines += [
            "",
            "## LLM run (optional)",
            "",
            f"- Intent: {intent_n}/{total}",
            f"- Phrase hit: {ans_n}/{total}",
            "",
            "| id | intent | answer | s |",
            "|---|---|---|---|",
        ]
        for r in payload["llm_rows"]:
            lines.append(
                f"| {r['id']} | {'ok' if r.get('intent_ok') else 'miss'} | "
                f"{'ok' if r.get('answer_ok') else 'miss'} | {r.get('elapsed_sec', '')} |"
            )
    else:
        lines += [
            "",
            "## LLM run",
            "",
            "Skipped. `python -m eval.run_eval --llm` needs GROQ_API_KEY.",
            "Phrase matching is not a faithfulness score.",
        ]
    RESULTS_MD.write_text("\n".join(lines) + "\n")


def main(with_llm: bool = False) -> None:
    gold = load_gold()
    df = load_default()
    pandas_part = run_pandas_eval(df, gold)
    facts = pandas_part["facts"]
    llm_rows = run_llm_eval(df, gold) if with_llm else []
    payload = {
        "pandas_rows": pandas_part["rows"],
        "llm_rows": llm_rows,
        "facts": facts,
        "summary": {
            "pandas_pass": pandas_part["pandas_pass"],
            "pandas_checked": pandas_part["pandas_checked"],
            "row_count": facts["row_count"],
            "cancel_rate": facts["cancel_rate"],
            "lead_canceled": facts["lead_by_cancel"]["canceled"],
            "lead_stayed": facts["lead_by_cancel"]["not_canceled"],
            "busiest_month": facts["busiest_month"],
        },
    }
    write_outputs(payload)
    print(
        f"pandas {pandas_part['pandas_pass']}/{pandas_part['pandas_checked']}  "
        f"rows={facts['row_count']} cancel={facts['cancel_rate']}%"
    )
    print(f"wrote {RESULTS_JSON} and {RESULTS_MD}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", action="store_true")
    args = parser.parse_args()
    main(with_llm=args.llm)
