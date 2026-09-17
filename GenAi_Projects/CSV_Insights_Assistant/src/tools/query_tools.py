"""Generic pandas extractors. Column names come from the current table, not a hotel schema."""

from __future__ import annotations

import pandas as pd

OPS = {
    ">": lambda col, val: col > val,
    "<": lambda col, val: col < val,
    ">=": lambda col, val: col >= val,
    "<=": lambda col, val: col <= val,
    "==": lambda col, val: col == val,
    "!=": lambda col, val: col != val,
    "contains": None,
}


def _coerce(series: pd.Series, value):
    if pd.api.types.is_numeric_dtype(series):
        try:
            num = float(value)
            return int(num) if num.is_integer() else num
        except (TypeError, ValueError):
            return value
    return value


def filter_rows(
    df: pd.DataFrame,
    column: str,
    operator: str,
    value,
) -> pd.DataFrame:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")
    if operator not in OPS:
        raise ValueError(f"Unsupported operator '{operator}'. Use {list(OPS)}")
    col = df[column]
    if operator == "contains":
        return df[col.astype(str).str.contains(str(value), case=False, na=False)]
    value = _coerce(col, value)
    return df[OPS[operator](col, value)]


def aggregate(
    df: pd.DataFrame,
    group_by: str,
    agg_column: str | None = None,
    agg_func: str = "count",
) -> pd.DataFrame:
    if group_by not in df.columns:
        raise ValueError(f"Group-by column '{group_by}' not found. Available: {list(df.columns)}")
    allowed = {"count", "mean", "sum", "min", "max", "median"}
    if agg_func not in allowed:
        raise ValueError(f"agg_func must be one of {sorted(allowed)}")
    if agg_column is None or agg_func == "count":
        return df.groupby(group_by, dropna=False).size().reset_index(name="count")
    if agg_column not in df.columns:
        raise ValueError(f"Aggregation column '{agg_column}' not found. Available: {list(df.columns)}")
    out = df.groupby(group_by, dropna=False)[agg_column].agg(agg_func).reset_index()
    out.columns = [group_by, f"{agg_func}_{agg_column}"]
    return out


def value_counts(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")
    vc = df[column].value_counts(dropna=False).head(n).reset_index()
    vc.columns = [column, "count"]
    return vc
