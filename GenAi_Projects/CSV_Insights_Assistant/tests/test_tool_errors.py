"""Tool exceptions must return strings, not crash the agent turn."""

from __future__ import annotations

from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage

from src.agents.data_analyst import create_data_analyst
from src.agents.viz_agent import create_viz_agent
from src.chart_buffer import ChartBuffer


class FakeToolLLM(GenericFakeChatModel):
    disable_streaming: bool = True

    def bind_tools(self, tools, **kw):
        return self


def _tool(executor, name: str):
    for t in executor.tools:
        if t.name == name:
            return t
    raise AssertionError(f"tool {name} not found")


def test_value_counts_bad_column_returns_error_string(sales_df):
    llm = FakeToolLLM(messages=iter([AIMessage(content="unused")]))
    analyst = create_data_analyst(sales_df, llm=llm)
    out = _tool(analyst, "tool_value_counts").invoke({"column": "Region"})
    assert isinstance(out, str)
    assert out.startswith("Tool error:")
    assert "not found" in out.lower() or "Region" in out


def test_sql_blocked_read_returns_error_string(sales_df):
    llm = FakeToolLLM(messages=iter([AIMessage(content="unused")]))
    analyst = create_data_analyst(sales_df, llm=llm)
    out = _tool(analyst, "tool_sql").invoke(
        {"query": "SELECT * FROM read_text('/etc/passwd')"}
    )
    assert isinstance(out, str)
    assert out.startswith("Tool error:")
    assert "rejected" in out.lower() or "allowed" in out.lower()


def test_sql_normal_select_still_works(sales_df):
    llm = FakeToolLLM(messages=iter([AIMessage(content="unused")]))
    analyst = create_data_analyst(sales_df, llm=llm)
    out = _tool(analyst, "tool_sql").invoke(
        {"query": "SELECT region, SUM(units) AS u FROM data GROUP BY region"}
    )
    assert isinstance(out, str)
    assert not out.startswith("Tool error:")
    assert "East" in out or "West" in out


def test_agent_turn_recovers_from_bad_tool_args(sales_df):
    """Wrong column → tool error string → LLM continues → final output, no crash."""
    llm = FakeToolLLM(
        messages=iter(
            [
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "tool_value_counts",
                            "args": {"column": "nope"},
                            "id": "1",
                        }
                    ],
                ),
                AIMessage(content="I could not find that column."),
            ]
        )
    )
    analyst = create_data_analyst(sales_df, llm=llm)
    result = analyst.invoke({"input": "counts by nope"})
    assert "output" in result
    assert isinstance(result["output"], str)


def test_viz_bad_column_returns_error_string(sales_df):
    llm = FakeToolLLM(messages=iter([AIMessage(content="unused")]))
    viz = create_viz_agent(sales_df, ChartBuffer(), llm=llm)
    out = _tool(viz, "tool_chart").invoke(
        {"chart_type": "bar", "x": "missing_col", "y": "count", "title": "x"}
    )
    assert out.startswith("Tool error:")
