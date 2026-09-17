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
