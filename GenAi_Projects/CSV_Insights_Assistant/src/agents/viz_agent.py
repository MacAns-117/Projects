"""Visualization agent — builds a Plotly figure and stashes it in ChartBuffer."""

from __future__ import annotations

import pandas as pd
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from src.chart_buffer import ChartBuffer
from src.config import MAX_ITERATIONS
from src.llm import get_llm
from src.schema import schema_card
from src.tools.viz_tools import compare_chart, generate_chart, prepare_plot_frame


def create_viz_agent(df: pd.DataFrame, buffer: ChartBuffer, llm=None) -> AgentExecutor:
    if llm is None:
        llm = get_llm()

    @tool
    def tool_chart(chart_type: str, x: str, y: str, title: str = "Chart") -> str:
        """Make a line, bar, or scatter chart.
        x is a column name. y is a column name, or 'count' to count rows per x."""
        plot_df = prepare_plot_frame(df, x=x, y=y)
        fig = generate_chart(plot_df, chart_type=chart_type, x=x, y=y, title=title)
        caption = f"{chart_type} chart: {title} ({y} by {x})"
        buffer.set(fig, caption)
        return f"Chart stored. {caption}. Rows plotted: {len(plot_df)}."

    @tool
    def tool_compare_chart(
        x: str,
        y: str,
        color: str,
        chart_type: str = "bar",
        title: str = "Comparison",
    ) -> str:
        """Grouped chart. color is the segment column. y may be a column or 'count'."""
        plot_df = prepare_plot_frame(df, x=x, y=y, color=color)
        fig = compare_chart(
            plot_df, x=x, y=y, color=color, chart_type=chart_type, title=title
        )
        caption = f"{chart_type} comparison: {title} ({y} by {x}, colored by {color})"
        buffer.set(fig, caption)
        return f"Chart stored. {caption}. Rows plotted: {len(plot_df)}."

    tools = [tool_chart, tool_compare_chart]
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You make charts for the current table.\n\n"
                + schema_card(df)
                + "\n\nCall one chart tool. Trends over a time-like column: line. "
                "Counts or categories: bar. Two numeric columns: scatter. "
                "Comparing segments: tool_compare_chart.",
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=MAX_ITERATIONS,
        verbose=False,
        handle_parsing_errors=True,
    )
