import pytest

from src.tools.query_tools import aggregate, filter_rows, value_counts
from src.tools.sql_tools import run_sql
from src.tools.stats_tools import compare_segments, compute_stats, correlation
from src.tools.viz_tools import compare_chart, generate_chart, prepare_plot_frame


class TestQuery:
    def test_filter_gt(self, sample_df):
        out = filter_rows(sample_df, "lead_time", ">", 50)
        assert len(out) == 2

    def test_filter_contains(self, sales_df):
        out = filter_rows(sales_df, "product", "contains", "Gadg")
        assert set(out["product"]) == {"Gadget"}

    def test_filter_bad_col(self, sample_df):
        with pytest.raises(ValueError, match="not found"):
            filter_rows(sample_df, "nope", ">", 0)

    def test_filter_bad_op(self, sample_df):
        with pytest.raises(ValueError, match="Unsupported"):
            filter_rows(sample_df, "lead_time", "like", 0)

    def test_aggregate_count(self, sample_df):
        out = aggregate(sample_df, group_by="hotel")
        assert "count" in out.columns
        assert out["count"].sum() == 5

    def test_aggregate_mean(self, sales_df):
        out = aggregate(sales_df, group_by="region", agg_column="units", agg_func="mean")
        assert "mean_units" in out.columns

    def test_value_counts(self, sales_df):
        out = value_counts(sales_df, "region", n=2)
        assert len(out) == 2


class TestStats:
    def test_mean_lead(self, sample_df):
        stats = compute_stats(sample_df, "lead_time")
        assert stats["mean"] == 58.0

    def test_grouped(self, sample_df):
        stats = compute_stats(sample_df, "adr", group_by="hotel")
        assert "City Hotel" in stats

    def test_non_numeric(self, sales_df):
        with pytest.raises(ValueError, match="not numeric"):
            compute_stats(sales_df, "region")

    def test_compare(self, sample_df):
        result = compare_segments(sample_df, "hotel", "is_canceled", "mean")
        assert abs(result["City Hotel"] - 0.6667) < 0.01

    def test_corr(self, sample_df):
        r = correlation(sample_df, "lead_time", "is_canceled")
        assert -1 <= r <= 1


class TestSql:
    def test_select(self, sales_df):
        out = run_sql(
            sales_df,
            "SELECT region, SUM(units) AS u FROM data GROUP BY region ORDER BY u DESC",
        )
        assert out.iloc[0]["region"] == "East"
        assert int(out.iloc[0]["u"]) == 19

    def test_rejects_insert(self, sales_df):
        with pytest.raises(ValueError, match="allowed"):
            run_sql(sales_df, "INSERT INTO data VALUES (1,1,1,1)")

    def test_rejects_drop(self, sales_df):
        with pytest.raises(ValueError, match="allowed"):
            run_sql(sales_df, "DROP TABLE data")

    def test_rejects_multi(self, sales_df):
        with pytest.raises(ValueError):
            run_sql(sales_df, "SELECT 1; SELECT 2")

    def test_rejects_read_text_passwd(self, sales_df):
        with pytest.raises(ValueError, match="allowed"):
            run_sql(sales_df, "SELECT * FROM read_text('/etc/passwd')")

    def test_rejects_read_csv_environ(self, sales_df):
        with pytest.raises(ValueError, match="allowed"):
            run_sql(sales_df, "SELECT * FROM read_csv('/proc/self/environ')")

    def test_rejects_glob_root(self, sales_df):
        with pytest.raises(ValueError, match="allowed"):
            run_sql(sales_df, "SELECT * FROM glob('/*')")

    def test_rejects_read_parquet(self, sales_df):
        with pytest.raises(ValueError, match="allowed"):
            run_sql(sales_df, "SELECT * FROM read_parquet('/tmp/x.parquet')")

    def test_rejects_proc_path_literal(self, sales_df):
        # Even a bare path mention in SQL is refused by the denylist.
        with pytest.raises(ValueError, match="allowed"):
            run_sql(sales_df, "SELECT '/proc/self/environ' AS p")

    def test_external_access_locked_even_if_denylist_bypassed(self, sales_df, monkeypatch):
        """DuckDB itself must refuse filesystem reads if the denylist were skipped."""
        import src.tools.sql_tools as sql_mod

        class _NeverMatch:
            def search(self, _s):
                return None

        monkeypatch.setattr(sql_mod, "_FORBIDDEN", _NeverMatch())
        with pytest.raises(Exception) as excinfo:
            sql_mod.run_sql(sales_df, "SELECT content FROM read_text('/etc/hostname')")
        msg = str(excinfo.value).lower()
        assert (
            "permission" in msg
            or "external" in msg
            or "denied" in msg
            or "not enabled" in msg
            or "disabled" in msg
        )

    def test_cannot_reenable_external_access(self):
        from src.tools.sql_tools import _connect

        con = _connect()
        try:
            with pytest.raises(Exception):
                con.execute("SET enable_external_access=true")
        finally:
            con.close()


class TestViz:
    def test_bar(self, sample_df):
        agg = aggregate(sample_df, group_by="hotel")
        fig = generate_chart(agg, "bar", "hotel", "count")
        assert fig.data[0].type == "bar"

    def test_prepare_count(self, sales_df):
        plot = prepare_plot_frame(sales_df, x="region", y="count")
        assert "count" in plot.columns
        assert plot["count"].sum() == 5

    def test_compare(self, sample_df):
        fig = compare_chart(
            sample_df, x="arrival_date_month", y="adr", color="hotel", chart_type="bar"
        )
        assert len(fig.data) == 2

    def test_bad_type(self, sample_df):
        with pytest.raises(ValueError):
            generate_chart(sample_df, "pie", "hotel", "adr")
