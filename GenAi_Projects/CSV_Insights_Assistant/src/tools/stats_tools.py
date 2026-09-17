"""Generic stats. Same functions on hotel bookings or any other table."""

from __future__ import annotations

import pandas as pd


def compute_stats(
    df: pd.DataFrame,
    column: str,
    group_by: str | None = None,
) -> dict:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' is not numeric.")

    def _stats(s: pd.Series) -> dict:
        return {
            "count": int(s.count()),
            "mean": float(s.mean()) if s.count() else None,
            "median": float(s.median()) if s.count() else None,
            "min": float(s.min()) if s.count() else None,
            "max": float(s.max()) if s.count() else None,
            "std": float(s.std()) if s.count() > 1 else None,
        }

    if group_by:
        if group_by not in df.columns:
            raise ValueError(f"Group-by column '{group_by}' not found. Available: {list(df.columns)}")
        return {str(k): _stats(g) for k, g in df.groupby(group_by, dropna=False)[column]}
    return _stats(df[column])


def compare_segments(
    df: pd.DataFrame,
    segment_col: str,
    metric_col: str,
    agg_func: str = "mean",
) -> dict:
    if segment_col not in df.columns:
        raise ValueError(f"Segment column '{segment_col}' not found. Available: {list(df.columns)}")
    if metric_col not in df.columns:
        raise ValueError(f"Metric column '{metric_col}' not found. Available: {list(df.columns)}")
    allowed = {"mean", "sum", "count", "median", "min", "max"}
    if agg_func not in allowed:
        raise ValueError(f"agg_func must be one of {sorted(allowed)}")
    result = df.groupby(segment_col, dropna=False)[metric_col].agg(agg_func)
    out = {}
    for k, v in result.items():
        try:
            out[str(k)] = round(float(v), 4)
        except (TypeError, ValueError):
            out[str(k)] = v
    return out


def correlation(df: pd.DataFrame, col1: str, col2: str) -> float:
    for col in (col1, col2):
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found. Available: {list(df.columns)}")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Column '{col}' is not numeric.")
    value = df[col1].corr(df[col2])
    if pd.isna(value):
        raise ValueError(f"Correlation of {col1} and {col2} is undefined (constant column?).")
    return float(value)
