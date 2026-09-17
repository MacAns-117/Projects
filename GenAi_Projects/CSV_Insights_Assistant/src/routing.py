"""Pure routing helpers — no LLM imports, so tests can load them cheaply."""

from __future__ import annotations


def classify_intent(text: str) -> str:
    token = text.strip().lower().split()[0] if text.strip() else "data"
    token = token.strip(".,:;")
    if token not in {"data", "viz", "both", "general"}:
        return "data"
    return token


def route_after_router(state: dict) -> str:
    intent = state["intent"]
    if intent == "viz":
        return "viz_agent"
    if intent == "general":
        return "report_writer"
    return "data_analyst"


def route_after_data_analyst(state: dict) -> str:
    if state["intent"] == "both":
        return "viz_agent"
    return "report_writer"
