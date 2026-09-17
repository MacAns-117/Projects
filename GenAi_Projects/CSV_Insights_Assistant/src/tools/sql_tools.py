"""Read-only SQL over the current table via DuckDB. Table name is always `data`."""

from __future__ import annotations

import re

import duckdb
import pandas as pd

from src.config import SQL_ROW_CAP

_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|attach|copy|create|replace|grant|pragma)\b",
    re.IGNORECASE,
)


def run_sql(df: pd.DataFrame, query: str, row_cap: int = SQL_ROW_CAP) -> pd.DataFrame:
    """Run a single SELECT/WITH query against the in-memory frame registered as `data`."""
    if not query or not query.strip():
        raise ValueError("Empty SQL.")
    stripped = query.strip().rstrip(";").strip()
    lowered = stripped.lower()
    if not (lowered.startswith("select") or lowered.startswith("with")):
        raise ValueError("Only SELECT / WITH queries are allowed. The table name is `data`.")
    if _FORBIDDEN.search(stripped):
        raise ValueError("Query rejected: only read-only SELECT/WITH is allowed.")
    if ";" in stripped:
        raise ValueError("One statement only.")
    con = duckdb.connect()
    try:
        con.register("data", df)
        result = con.execute(stripped).df()
    finally:
        con.close()
    if len(result) > row_cap:
        result = result.head(row_cap)
        result.attrs["truncated"] = True
        result.attrs["row_cap"] = row_cap
    return result
