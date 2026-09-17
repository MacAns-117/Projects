from src.schema import infer_kind, schema_card


def test_schema_lists_columns(sample_df):
    card = schema_card(sample_df)
    assert "rows=5" in card
    assert "lead_time" in card
    assert "numeric" in card


def test_infer_kinds(sales_df):
    assert infer_kind(sales_df["units"]) == "numeric"
    assert infer_kind(sales_df["region"]) == "categorical"


def test_schema_on_sales(sales_df):
    card = schema_card(sales_df)
    assert "product" in card
    assert "hotel" not in card
