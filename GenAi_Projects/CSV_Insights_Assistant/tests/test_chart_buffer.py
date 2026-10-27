from src.chart_buffer import ChartBuffer
from src.tools.viz_tools import generate_chart, prepare_plot_frame


def test_buffer_holds_figure(sales_df):
    buf = ChartBuffer()
    plot = prepare_plot_frame(sales_df, x="region", y="count")
    fig = generate_chart(plot, "bar", "region", "count", title="Units")
    buf.set(fig, "bar: Units")
    got, cap = buf.snapshot()
    assert got is fig
    assert "Units" in cap


def test_buffer_clear_drops_figure(sales_df):
    buf = ChartBuffer()
    plot = prepare_plot_frame(sales_df, x="region", y="count")
    fig = generate_chart(plot, "bar", "region", "count", title="Units")
    buf.set(fig, "bar: Units")
    buf.clear()
    got, cap = buf.snapshot()
    assert got is None
    assert cap == ""


def test_orchestrator_clears_chart_between_turns(sales_df):
    """A turn that draws no chart must not reuse the previous turn's figure."""
    from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
    from langchain_core.messages import AIMessage

    from src.chart_buffer import ChartBuffer
    from src.orchestrator import create_orchestrator, empty_state

    class FakeToolLLM(GenericFakeChatModel):
        disable_streaming: bool = True

        def bind_tools(self, tools, **kw):
            return self

    buf = ChartBuffer()
    # Turn 1: router=viz → chart tool → report
    # Turn 2: router=viz → plain text (no tool) → report  → chart must be None
    seq = [
        AIMessage(content="viz"),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "tool_chart",
                    "args": {
                        "chart_type": "bar",
                        "x": "region",
                        "y": "count",
                        "title": "T1",
                    },
                    "id": "a",
                }
            ],
        ),
        AIMessage(content="ok"),
        AIMessage(content="report1"),
        AIMessage(content="viz"),
        AIMessage(content="I cannot make that chart."),
        AIMessage(content="report2"),
    ]
    llm = FakeToolLLM(messages=iter(seq))
    graph = create_orchestrator(sales_df, llm=llm, chart_buffer=buf)
    r1 = graph.invoke(empty_state("chart counts by region"))
    assert r1["chart_fig"] is not None
    r2 = graph.invoke(empty_state("plot something impossible"))
    assert r2["chart_fig"] is None
