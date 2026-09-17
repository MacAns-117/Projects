"""Infer a schema card from any DataFrame so the agents are not hotel-specific."""

from __future__ import annotations

import pandas as pd

MAX_EXAMPLE_VALUES = 6
MAX_CARD_CHARS = 4_000


def infer_kind(series: pd.Series) -> str:
    """Rough column kind for the prompt: numeric, datetime, boolean, categorical, text."""
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_numeric_dtype(series):
        nunique = int(series.nunique(dropna=True))
        if nunique <= 2:
            return "numeric/flag"
        return "numeric"
    nunique = int(series.nunique(dropna=True))
    if nunique <= 40:
        return "categorical"
    return "text"


def schema_card(df: pd.DataFrame) -> str:
    """Human-readable schema the LLM sees before it picks tools."""
    lines = [
        f"rows={len(df):,}  columns={len(df.columns)}",
        "name | dtype | kind | non_null | nunique | examples",
    ]
    for col in df.columns:
        s = df[col]
        kind = infer_kind(s)
        examples = (
            s.dropna()
            .astype(str)
            .unique()[:MAX_EXAMPLE_VALUES]
            .tolist()
        )
        example_str = ", ".join(examples)
        if len(example_str) > 80:
            example_str = example_str[:77] + "..."
        lines.append(
            f"{col} | {s.dtype} | {kind} | {int(s.notna().sum())} | "
            f"{int(s.nunique(dropna=True))} | {example_str}"
        )
    card = "\n".join(lines)
    if len(card) > MAX_CARD_CHARS:
        card = card[: MAX_CARD_CHARS - 20] + "\n... (truncated)"
    return card


def numeric_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def categorical_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if infer_kind(df[c]) in ("categorical", "boolean", "text")]
