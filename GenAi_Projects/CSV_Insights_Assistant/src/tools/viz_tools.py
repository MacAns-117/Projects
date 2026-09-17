"""Plotly charts. Callers pass an already-aggregated frame when they can."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from src.config import CHART_POINT_CAP

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def _maybe_order_months(df: pd.DataFrame, col: str) -> pd.DataFrame:
    values = set(df[col].dropna().astype(str).unique())
    if values and values <= set(MONTH_ORDER):
        out = df.copy()
        out[col] = pd.Categorical(out[col].astype(str), categories=MONTH_ORDER, ordered=True)
        return out.sort_values(col)
    return df


def _cap(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) > CHART_POINT_CAP:
        return df.head(CHART_POINT_CAP)
    return df


def generate_chart(
    df: pd.DataFrame,
    chart_type: str,
    x: str,
    y: str,
    title: str = "Chart",
) -> go.Figure:
    if x not in df.columns:
        raise ValueError(f"X column '{x}' not found. Available: {list(df.columns)}")
    if y not in df.columns:
        raise ValueError(f"Y column '{y}' not found. Available: {list(df.columns)}")
    plot_df = _cap(_maybe_order_months(df, x))
    if chart_type == "line":
        fig = go.Figure(go.Scatter(x=plot_df[x], y=plot_df[y], mode="lines+markers"))
    elif chart_type == "bar":
        fig = go.Figure(go.Bar(x=plot_df[x], y=plot_df[y]))
    elif chart_type == "scatter":
        fig = go.Figure(go.Scatter(x=plot_df[x], y=plot_df[y], mode="markers"))
    else:
        raise ValueError("chart_type must be 'line', 'bar', or 'scatter'.")
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
        template="plotly_white",
        height=450,
    )
    return fig


def compare_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str,
    chart_type: str = "bar",
    title: str = "Comparison",
) -> go.Figure:
    for col in (x, y, color):
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found. Available: {list(df.columns)}")
    plot_df = _cap(_maybe_order_months(df, x))
    fig = go.Figure()
    for seg in plot_df[color].dropna().unique():
        seg_df = plot_df[plot_df[color] == seg]
        if chart_type == "bar":
            fig.add_trace(go.Bar(x=seg_df[x], y=seg_df[y], name=str(seg)))
        elif chart_type == "line":
            fig.add_trace(
                go.Scatter(x=seg_df[x], y=seg_df[y], mode="lines+markers", name=str(seg))
            )
        else:
            raise ValueError("chart_type must be 'bar' or 'line'.")
    fig.update_layout(
        title=title,
        xaxis_title=x,
        yaxis_title=y,
        barmode="group",
        template="plotly_white",
        height=450,
    )
    return fig


def prepare_plot_frame(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
) -> pd.DataFrame:
    """If y is not a column, treat it as a count and group. Used by the viz agent."""
    if x not in df.columns:
        raise ValueError(f"X column '{x}' not found. Available: {list(df.columns)}")
    if color and color not in df.columns:
        raise ValueError(f"Color column '{color}' not found. Available: {list(df.columns)}")
    if y in df.columns:
        cols = [x, y] + ([color] if color else [])
        return df[cols].dropna()
    # y is a label such as "count"
    if color:
        out = df.groupby([x, color], dropna=False).size().reset_index(name=y)
    else:
        out = df.groupby(x, dropna=False).size().reset_index(name=y)
    return out
