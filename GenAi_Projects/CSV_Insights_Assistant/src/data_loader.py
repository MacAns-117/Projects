"""Load any CSV into a DataFrame. Hotel-only rules run only when those columns exist."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import DEFAULT_CSV, DROP_DUPLICATES, MAX_ROWS, MAX_UPLOAD_MB


def _drop_unnamed_index(df: pd.DataFrame) -> pd.DataFrame:
    drop = [c for c in df.columns if str(c).startswith("Unnamed")]
    return df.drop(columns=drop) if drop else df


def _maybe_drop_zero_guests(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    guest_cols = [c for c in ("adults", "children", "babies") if c in df.columns]
    if len(guest_cols) < 3:
        return df, 0
    filled = df[guest_cols].fillna(0)
    mask = filled.sum(axis=1) == 0
    n = int(mask.sum())
    if n:
        df = df.loc[~mask].copy()
    return df, n


def _parse_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    """Parse string date columns only. Never coerce numeric year/month fields."""
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            continue
        sample = df[col].dropna().astype(str).head(30)
        if sample.empty:
            continue
        if not sample.str.contains(r"\d{4}[-/]").any():
            continue
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().mean() >= 0.8:
            df[col] = parsed
    return df


def clean_frame(df: pd.DataFrame, *, drop_duplicates: bool = DROP_DUPLICATES) -> pd.DataFrame:
    df = _drop_unnamed_index(df)
    if drop_duplicates:
        df = df.drop_duplicates()
    df, _ = _maybe_drop_zero_guests(df)
    for col in ("children", "babies"):
        if col in df.columns:
            df[col] = df[col].fillna(0)
    df = _parse_datetimes(df)
    df = df.reset_index(drop=True)
    return df


def load_csv(path: str | Path, *, drop_duplicates: bool = DROP_DUPLICATES) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_UPLOAD_MB:
        raise ValueError(f"File is {size_mb:.1f} MB; cap is {MAX_UPLOAD_MB} MB.")
    df = pd.read_csv(path)
    if len(df) > MAX_ROWS:
        raise ValueError(f"{len(df):,} rows exceeds the {MAX_ROWS:,} row cap.")
    return clean_frame(df, drop_duplicates=drop_duplicates)


def load_csv_buffer(buffer, filename: str = "upload.csv") -> pd.DataFrame:
    buffer.seek(0)
    df = pd.read_csv(buffer)
    if len(df) > MAX_ROWS:
        raise ValueError(f"{len(df):,} rows exceeds the {MAX_ROWS:,} row cap.")
    df = clean_frame(df)
    df.attrs["source_name"] = filename
    return df


def load_default() -> pd.DataFrame:
    df = load_csv(DEFAULT_CSV)
    df.attrs["source_name"] = DEFAULT_CSV.name
    return df
