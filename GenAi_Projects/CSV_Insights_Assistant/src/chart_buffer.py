"""Side channel for Plotly figures.

LangChain tools return strings to the LLM. The figure itself is stashed here
so Streamlit can render it. One figure per turn (last write wins).
Clear the buffer at the start of every user turn so a prior chart never leaks.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import plotly.graph_objects as go


@dataclass
class ChartBuffer:
    figure: go.Figure | None = None
    caption: str = ""
    history: list[str] = field(default_factory=list)

    def set(self, fig: go.Figure, caption: str) -> None:
        self.figure = fig
        self.caption = caption
        self.history.append(caption)

    def clear(self) -> None:
        """Drop the current figure/caption (history is kept for debugging)."""
        self.figure = None
        self.caption = ""

    def snapshot(self) -> tuple[go.Figure | None, str]:
        return self.figure, self.caption
