import json
from pathlib import Path

from src.data_loader import load_default
from eval.run_eval import check_fact, load_gold, pandas_facts, run_pandas_eval

GOLD = Path(__file__).resolve().parent.parent / "eval" / "gold_questions.json"


def test_gold_count_and_ids():
    qs = json.loads(GOLD.read_text())
    assert len(qs) == 20
    ids = [q["id"] for q in qs]
    assert len(ids) == len(set(ids))
    assert all("question" in q and "intent" in q for q in qs)
    assert all(q["intent"] in {"data", "viz", "both", "general"} for q in qs)


def test_no_2021_in_gold():
    text = GOLD.read_text()
    assert "2021" not in text


def test_pandas_facts_match_gold():
    df = load_default()
    gold = load_gold()
    result = run_pandas_eval(df, gold)
    assert result["pandas_pass"] == result["pandas_checked"]
    facts = pandas_facts(df)
    assert facts["row_count"] == 87230
    assert abs(facts["cancel_rate"] - 27.52) < 0.05
    assert facts["busiest_month"] == "August"
    assert check_fact("lead_by_cancel", {"canceled": 105.7, "not_canceled": 70.2}, facts)
