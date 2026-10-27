"""Lightweight faithfulness / groundedness judge (LLM-as-judge).

Works against any OpenAI-compatible chat endpoint. By default it reuses the
app's own LLM settings (see src/llm.py), so one set of env vars drives both
answer generation and judging:

  LLM_PROVIDER=groq (default)   judge = Groq's OpenAI-compatible endpoint,
                                GROQ_API_KEY, LLM_MODEL or openai/gpt-oss-120b
  LLM_PROVIDER=openai_compatible
                                judge = LLM_BASE_URL / LLM_API_KEY / LLM_MODEL

Optional judge-only overrides (e.g. local generation, stronger hosted judge):
  OPENAI_BASE_URL   e.g. https://api.groq.com/openai/v1  or http://127.0.0.1:8080/v1
  OPENAI_API_KEY    bearer token for OPENAI_BASE_URL
  JUDGE_MODEL       judge model id

Does not call paid APIs from CI. Pass a ``judge_fn`` in tests to mock.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Callable, Iterable, Mapping

from src.chain import REFUSAL

JUDGE_RUBRIC = """You are a strict faithfulness grader for a RAG system.

Given a QUESTION, an ANSWER, and the CONTEXT CHUNKS the answer was allowed to use,
decide whether the answer is fully supported.

Rubric:
- grounded = true  iff every factual claim in the ANSWER is entailed by the CONTEXT.
- grounded = false if the ANSWER invents facts, contradicts the CONTEXT, or answers
  an out-of-scope question instead of refusing.
- For out-of-scope questions (clearly unrelated to the CONTEXT), the ANSWER must be
  a refusal equivalent to "I don't know based on the provided context."
  A refusal → grounded = true. An attempted answer → grounded = false.

Return ONLY a JSON object: {"grounded": true|false, "reason": "<one short sentence>"}
No markdown fences.
"""

JudgeFn = Callable[[str], str]


@dataclass
class FaithfulnessResult:
    question_id: str
    question: str
    answer: str
    grounded: bool
    reason: str
    out_of_scope: bool
    refused: bool


def is_refusal(answer: str) -> bool:
    text = (answer or "").strip().lower()
    if not text:
        return False
    if REFUSAL.lower() in text:
        return True
    needles = (
        "i don't know",
        "i do not know",
        "cannot answer",
        "can't answer",
        "not in the",
        "no relevant",
        "provided context",
    )
    return any(n in text for n in needles)


def build_judge_prompt(question: str, answer: str, context: str) -> str:
    return (
        f"{JUDGE_RUBRIC}\n\n"
        f"QUESTION:\n{question}\n\n"
        f"ANSWER:\n{answer}\n\n"
        f"CONTEXT:\n{context}\n\n"
        "JSON:"
    )


def parse_judge_json(raw: str) -> tuple[bool, str]:
    """Parse judge output into (grounded, reason). Raises ValueError on garbage."""
    text = (raw or "").strip()
    if not text:
        raise ValueError("empty judge response")
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError(f"not JSON: {text[:120]}")
        data = json.loads(match.group(0))
    if not isinstance(data, dict) or "grounded" not in data:
        raise ValueError(f"missing grounded: {data!r}")
    grounded = bool(data["grounded"])
    reason = str(data.get("reason", "")).strip() or "(no reason)"
    return grounded, reason


GROQ_OPENAI_BASE_URL = "https://api.groq.com/openai/v1"
JUDGE_DEFAULT_MAX_TOKENS = 256


@dataclass(frozen=True)
class JudgeSettings:
    base_url: str
    model: str
    api_key: str = field(repr=False)
    max_tokens: int = JUDGE_DEFAULT_MAX_TOKENS


def resolve_judge_settings(env: Mapping[str, str] | None = None) -> JudgeSettings:
    """Pick the judge endpoint. Explicit OPENAI_* / JUDGE_MODEL win; else LLM_* vars.

    Never sends GROQ_API_KEY anywhere except api.groq.com. Raises RuntimeError
    when nothing usable is configured.
    """
    from src.llm import DEFAULT_LLM_MODEL, resolve_llm_settings

    env = os.environ if env is None else env

    def g(k: str) -> str:
        return (env.get(k) or "").strip()

    judge_model = g("JUDGE_MODEL")
    max_tokens = JUDGE_DEFAULT_MAX_TOKENS
    if g("LLM_MAX_TOKENS").isdigit():
        max_tokens = max(int(g("LLM_MAX_TOKENS")), JUDGE_DEFAULT_MAX_TOKENS)

    explicit_base = g("OPENAI_BASE_URL").rstrip("/")
    if explicit_base:
        groq_host = "api.groq.com" in explicit_base
        key = (
            g("OPENAI_API_KEY")
            or (g("GROQ_API_KEY") if groq_host else g("LLM_API_KEY"))
            or "local"  # llama.cpp / Ollama ignore the key
        )
        model = judge_model or g("LLM_MODEL") or DEFAULT_LLM_MODEL
        return JudgeSettings(explicit_base, model, key, max_tokens)

    try:
        s = resolve_llm_settings(env)
    except ValueError as exc:
        raise RuntimeError(f"Faithfulness judge not configured: {exc}") from exc

    if s.provider == "openai_compatible":
        return JudgeSettings(s.base_url, judge_model or s.model, s.api_key, max_tokens)

    key = s.api_key or (g("OPENAI_API_KEY") if g("OPENAI_API_KEY").startswith("gsk_") else "")
    if not key:
        raise RuntimeError(
            "No judge endpoint configured. Set GROQ_API_KEY (Groq default), or "
            "LLM_PROVIDER=openai_compatible + LLM_BASE_URL + LLM_MODEL for a local "
            "server, or OPENAI_BASE_URL (+ OPENAI_API_KEY, JUDGE_MODEL) for a judge-only endpoint."
        )
    return JudgeSettings(GROQ_OPENAI_BASE_URL, judge_model or s.model, key, max_tokens)


def default_openai_judge(prompt: str) -> str:
    """Call an OpenAI-compatible Chat Completions endpoint."""
    from src.llm import strip_reasoning

    js = resolve_judge_settings()

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The 'openai' package is required for the faithfulness judge "
            "(pip install openai). It talks to any OpenAI-compatible endpoint."
        ) from exc

    client = OpenAI(base_url=js.base_url, api_key=js.api_key)
    resp = client.chat.completions.create(
        model=js.model,
        temperature=0,
        max_tokens=js.max_tokens,
        messages=[
            {"role": "system", "content": "Return only the JSON object requested."},
            {"role": "user", "content": prompt},
        ],
    )
    return strip_reasoning(resp.choices[0].message.content or "")


def grade_one(
    question: str,
    answer: str,
    context: str,
    *,
    question_id: str = "",
    out_of_scope: bool = False,
    judge_fn: JudgeFn | None = None,
) -> FaithfulnessResult:
    """Grade a single answer. OOS refusals short-circuit as grounded without an LLM."""
    refused = is_refusal(answer)
    if out_of_scope:
        return FaithfulnessResult(
            question_id=question_id,
            question=question,
            answer=answer,
            grounded=refused,
            reason="OOS refusal" if refused else "OOS question was answered instead of refused",
            out_of_scope=True,
            refused=refused,
        )

    fn = judge_fn or default_openai_judge
    prompt = build_judge_prompt(question, answer, context)
    raw = fn(prompt)
    grounded, reason = parse_judge_json(raw)
    return FaithfulnessResult(
        question_id=question_id,
        question=question,
        answer=answer,
        grounded=grounded,
        reason=reason,
        out_of_scope=False,
        refused=refused,
    )


def summarize(results: Iterable[FaithfulnessResult]) -> dict:
    rows = list(results)
    n = len(rows)
    grounded_n = sum(1 for r in rows if r.grounded)
    oos = [r for r in rows if r.out_of_scope]
    oos_ok = sum(1 for r in oos if r.grounded)
    in_scope = [r for r in rows if not r.out_of_scope]
    in_ok = sum(1 for r in in_scope if r.grounded)
    return {
        "n": n,
        "grounded_rate": round(grounded_n / n, 4) if n else 0.0,
        "grounded": grounded_n,
        "in_scope_n": len(in_scope),
        "in_scope_grounded": in_ok,
        "in_scope_rate": round(in_ok / len(in_scope), 4) if in_scope else 0.0,
        "oos_n": len(oos),
        "oos_ok": oos_ok,
        "oos_refuse_rate": round(oos_ok / len(oos), 4) if oos else 0.0,
    }
