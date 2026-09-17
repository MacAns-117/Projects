"""Side channel for Plotly figures.

LangChain tools return strings to the LLM. The figure itself is stashed here
so Streamlit can render it. One figure per turn (last write wins).
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

    def snapshot(self) -> tuple[go.Figure | None, str]:
        return self.figure, self.caption
