"""Faithfulness judge unit tests — mocked judge, no network."""

from __future__ import annotations

import pytest

from eval.faithfulness import (
    grade_one,
    is_refusal,
    parse_judge_json,
    summarize,
)
from src.chain import REFUSAL


def test_parse_judge_json_plain_and_fenced():
    assert parse_judge_json('{"grounded": true, "reason": "ok"}') == (True, "ok")
    assert parse_judge_json('```json\n{"grounded": false, "reason": "hallucinated"}\n```') == (
        False,
        "hallucinated",
    )


def test_parse_judge_json_garbage():
    with pytest.raises(ValueError):
        parse_judge_json("not json")


def test_is_refusal():
    assert is_refusal(REFUSAL)
    assert is_refusal("I don't know based on the provided context.")
    assert not is_refusal("The Transformer has 6 layers [1].")


def test_oos_refusal_short_circuits_without_judge():
    called = {"n": 0}

    def judge(_prompt: str) -> str:
        called["n"] += 1
        return '{"grounded": true, "reason": "should not run"}'

    r = grade_one(
        "What is the capital of France?",
        REFUSAL,
        context="No relevant context found.",
        question_id="oos-paris",
        out_of_scope=True,
        judge_fn=judge,
    )
    assert r.grounded is True
    assert r.refused is True
    assert called["n"] == 0


def test_oos_answer_is_not_grounded():
    r = grade_one(
        "What is the capital of France?",
        "Paris is the capital of France.",
        context="No relevant context found.",
        question_id="oos-paris",
        out_of_scope=True,
        judge_fn=lambda p: '{"grounded": true, "reason": "unused"}',
    )
    assert r.grounded is False


def test_in_scope_uses_mocked_judge():
    r = grade_one(
        "How many encoder layers?",
        "N = 6 [1].",
        context="[1] attention.pdf, p.3\nThe encoder has N = 6 identical layers.",
        question_id="att-encoder-n",
        out_of_scope=False,
        judge_fn=lambda p: '{"grounded": true, "reason": "supported by [1]"}',
    )
    assert r.grounded is True
    assert "supported" in r.reason


def test_summarize_rates():
    rows = [
        grade_one("q1", REFUSAL, "", question_id="o1", out_of_scope=True),
        grade_one(
            "q2",
            "ans",
            "ctx",
            question_id="i1",
            out_of_scope=False,
            judge_fn=lambda p: '{"grounded": false, "reason": "no"}',
        ),
    ]
    s = summarize(rows)
    assert s["n"] == 2
    assert s["oos_ok"] == 1
    assert s["in_scope_grounded"] == 0
