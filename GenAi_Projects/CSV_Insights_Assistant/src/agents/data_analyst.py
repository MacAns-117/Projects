"""Data analyst — tool-calling over whatever DataFrame is loaded."""

from __future__ import annotations

import pandas as pd
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from src.config import MAX_ITERATIONS
from src.llm import get_llm
from src.schema import schema_card
from src.tools.query_tools import aggregate, filter_rows, value_counts
from src.tools.sql_tools import run_sql
from src.tools.stats_tools import compare_segments, compute_stats, correlation


def _preview(frame: pd.DataFrame, n: int = 8) -> str:
    extra = ""
    if frame.attrs.get("truncated"):
        extra = f"\n(truncated to {frame.attrs.get('row_cap')} rows)"
    return f"{len(frame)} rows, columns {list(frame.columns)}{extra}\n{frame.head(n).to_string()}"


def create_data_analyst(df: pd.DataFrame, llm=None) -> AgentExecutor:
    if llm is None:
        llm = get_llm()

    @tool
    def tool_filter(column: str, operator: str, value: str) -> str:
        """Filter rows. operator is one of >, <, ==, >=, <=, !=, contains."""
        result = filter_rows(df, column=column, operator=operator, value=value)
        return _preview(result)

    @tool
    def tool_aggregate(group_by: str, agg_column: str = "", agg_func: str = "count") -> str:
        """Group-by aggregation. agg_func: count, mean, sum, min, max, median.
        Leave agg_column empty when counting rows."""
        col = agg_column or None
        result = aggregate(df, group_by=group_by, agg_column=col, agg_func=agg_func)
        return result.to_string(index=False)

    @tool
    def tool_value_counts(column: str, n: int = 10) -> str:
        """Top-n value counts for a column."""
        result = value_counts(df, column=column, n=n)
        return result.to_string(index=False)

    @tool
    def tool_stats(column: str, group_by: str = "") -> str:
        """Mean/median/min/max/std for a numeric column, optionally grouped."""
        gb = group_by or None
        return str(compute_stats(df, column=column, group_by=gb))

    @tool
    def tool_compare(segment_col: str, metric_col: str, agg_func: str = "mean") -> str:
        """Compare a metric across segments."""
        return str(compare_segments(df, segment_col, metric_col, agg_func))

    @tool
    def tool_correlation(col1: str, col2: str) -> str:
        """Pearson correlation between two numeric columns."""
        r = correlation(df, col1, col2)
        return f"corr({col1}, {col2}) = {r:.4f}"

    @tool
    def tool_sql(query: str) -> str:
        """Read-only SQL. Table name is `data`. SELECT/WITH only. Result capped."""
        result = run_sql(df, query)
        return _preview(result, n=15)

    tools = [
        tool_filter,
        tool_aggregate,
        tool_value_counts,
        tool_stats,
        tool_compare,
        tool_correlation,
        tool_sql,
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a data analyst for a single in-memory table.\n\n"
                + schema_card(df)
                + "\n\nTools talk to this table only. Prefer a small number of tool calls. "
                "Use tool_sql when a filter+group is awkward in one pandas call. "
                "The SQL table name is `data`. Cite numbers from tool results. "
                "If the table cannot answer, say so. Do not invent values.",
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
