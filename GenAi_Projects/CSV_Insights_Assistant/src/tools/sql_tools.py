"""Read-only SQL over the current table via DuckDB. Table name is always `data`."""

from __future__ import annotations

import re

import duckdb
import pandas as pd

from src.config import SQL_ROW_CAP

# Keyword denylist — defence in depth on top of DuckDB's enable_external_access=False.
# Covers DDL/DML plus file/system readers that must never touch the host.
_FORBIDDEN = re.compile(
    r"\b("
    r"insert|update|delete|drop|alter|attach|copy|create|replace|grant|pragma|"
    r"read_text|read_blob|read_csv|read_csv_auto|read_parquet|read_json|"
    r"read_json_auto|read_ndjson|glob"
    r")\b"
    r"|/proc",
    re.IGNORECASE,
)


def _connect() -> duckdb.DuckDBPyConnection:
    """In-memory DuckDB with filesystem / HTTP access locked off."""
    # lock_configuration=True prevents SET enable_external_access=true later.
    return duckdb.connect(
        config={
            "enable_external_access": False,
            "lock_configuration": True,
        }
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
    con = _connect()
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
