"""
Evaluation runner — tests the AI Research Agent on 15 gold questions.

For each question, checks if the final report contains expected key phrases.
Outputs results to eval/results.json and eval/results.md.

Usage:
    python -m eval.run_eval           # live run (requires API keys; PAID)
    python -m eval.run_eval --mock    # smoke scorer without API calls

Note: Live mode makes 100+ API calls (15 questions x full pipeline) and
takes 30-60 minutes to complete. Run it once and commit the results.
Without keys (and without --mock), the runner skips with a clear message.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from src.config import validate_config
from src.orchestrator import create_orchestrator


EVAL_DIR = Path(__file__).resolve().parent
GOLD_FILE = EVAL_DIR / "gold_questions.json"
RESULTS_JSON = EVAL_DIR / "results.json"
RESULTS_MD = EVAL_DIR / "results.md"


def load_gold_questions() -> list[dict]:
    with open(GOLD_FILE, "r") as f:
        return json.load(f)


def check_report_quality(report: str, expected_phrases: list[str]) -> bool:
    """Check if the report contains all expected key phrases (case-insensitive)."""
    report_lower = report.lower()
    return all(phrase.lower() in report_lower for phrase in expected_phrases)


def run_mock_evaluation() -> dict:
    """Smoke the scorer and gold file without calling paid APIs."""
    print("=" * 70)
    print("AI Research Agent — Mock Evaluation (no API calls)")
    print("=" * 70)

    questions = load_gold_questions()
    print(f"\n✓ Loaded {len(questions)} gold questions\n")

    results = []
    correct = 0
    for i, q in enumerate(questions, 1):
        expected = q.get("expected_phrases", [])
        # Synthetic report that includes all expected phrases → always matches
        fake_report = "Mock report. " + " ".join(expected)
        match = check_report_quality(fake_report, expected)
        # Also verify a negative case: empty report must fail when phrases exist
        empty_match = check_report_quality("", expected)
        assert match is True
        assert empty_match is False

        if match:
            correct += 1

        results.append({
            "id": q["id"],
            "question": q["question"],
            "expected_phrases": expected,
            "report_match": match,
            "elapsed_sec": 0.0,
            "sources_found": 0,
            "report_preview": fake_report[:300],
            "mode": "mock",
        })
        print(f"  [{i}/{len(questions)}] {q['id']}: scorer smoke ✓")

    summary = {
        "total_questions": len(questions),
        "accuracy": round(correct / len(questions) * 100, 1) if questions else 0,
        "correct": correct,
        "avg_time_sec": 0.0,
        "mode": "mock",
    }
    print(f"\n✓ Mock eval OK — scorer + gold file smoke passed ({correct}/{len(questions)})")
    return {"results": results, "summary": summary}


def run_evaluation() -> dict:
    print("=" * 70)
    print("AI Research Agent — Evaluation Run")
    print("=" * 70)

    validate_config()
    print("\n✓ Config validated")

    print("\nCreating orchestrator...")
    orchestrator = create_orchestrator()
    print("✓ Orchestrator ready")

    questions = load_gold_questions()
    print(f"\n✓ Loaded {len(questions)} gold questions\n")

    results = []
    correct = 0
    total = len(questions)

    for i, q in enumerate(questions, 1):
        q_id = q["id"]
        question = q["question"]
        expected = q.get("expected_phrases", [])

        print(f"\n[{i}/{total}] {q_id}: {question[:60]}...")

        try:
            start = time.time()
            state = orchestrator.invoke({
                "question": question,
                "context": "",
                "search_queries": [],
                "sources": [],
                "sources_text": "",
                "synthesis": "",
                "final_report": "",
            })
            elapsed = time.time() - start

            report = state.get("final_report", "")
            match = check_report_quality(report, expected)

            if match:
                correct += 1

            result = {
                "id": q_id,
                "question": question,
                "expected_phrases": expected,
                "report_match": match,
                "elapsed_sec": round(elapsed, 1),
                "sources_found": len(state.get("sources", [])),
                "report_preview": report[:300] + "..." if len(report) > 300 else report,
            }

            status = "✓" if match else "✗"
            print(f"  {status} Match: {match} | Sources: {len(state.get('sources', []))} | {elapsed:.1f}s")

        except Exception as e:
            result = {
                "id": q_id,
                "question": question,
                "error": str(e),
                "report_match": False,
            }
            print(f"  ✗ ERROR: {e}")

        results.append(result)

    summary = {
        "total_questions": total,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0,
        "correct": correct,
        "avg_time_sec": round(sum(r.get("elapsed_sec", 0) for r in results) / total, 1) if total > 0 else 0,
    }

    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Report quality accuracy: {summary['accuracy']}% ({correct}/{total})")
    print(f"  Average time per question: {summary['avg_time_sec']}s")
    print(f"{'=' * 70}")

    return {"results": results, "summary": summary}


def write_results(eval_data: dict) -> None:
    with open(RESULTS_JSON, "w") as f:
        json.dump(eval_data, f, indent=2)
    print(f"\n✓ Wrote {RESULTS_JSON}")

    md_lines = [
        "# AI Research Agent — Evaluation Results\n",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n",
        f"**Mode:** {eval_data['summary'].get('mode', 'live')}\n",
        "## Summary\n",
        f"- **Total questions:** {eval_data['summary']['total_questions']}",
        f"- **Report accuracy:** {eval_data['summary']['accuracy']}% ({eval_data['summary']['correct']}/{eval_data['summary']['total_questions']})",
        f"- **Avg time per question:** {eval_data['summary']['avg_time_sec']}s\n",
        "## Per-question results\n",
        "| # | ID | Match | Sources | Time (s) |",
        "|---|---|---|---|---|",
    ]

    for i, r in enumerate(eval_data["results"], 1):
        match = "✓" if r.get("report_match") else "✗"
        sources = r.get("sources_found", 0)
        t = r.get("elapsed_sec", 0)
        md_lines.append(f"| {i} | {r['id']} | {match} | {sources} | {t} |")

    with open(RESULTS_MD, "w") as f:
        f.write("\n".join(md_lines))
    print(f"✓ Wrote {RESULTS_MD}")


def _has_api_keys() -> bool:
    return bool(os.getenv("GROQ_API_KEY")) and bool(os.getenv("TAVILY_API_KEY"))


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Research Agent evaluation runner")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Smoke the phrase-match scorer without calling APIs",
    )
    args = parser.parse_args()

    if args.mock:
        eval_data = run_mock_evaluation()
        write_results(eval_data)
        print("\n✓ Mock evaluation complete.")
        return

    if not _has_api_keys():
        print(
            "Skipping live eval: GROQ_API_KEY and/or TAVILY_API_KEY not set.\n"
            "Use --mock to smoke the scorer, or set keys for a live (paid) run."
        )
        return

    eval_data = run_evaluation()
    write_results(eval_data)
    print("\n✓ Evaluation complete.")


if __name__ == "__main__":
    main()
