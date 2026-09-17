import pandas as pd
from io import StringIO

from src.data_loader import clean_frame, load_csv_buffer, load_default


def test_clean_drops_zero_guests(sample_df):
    extra = sample_df.iloc[[0]].copy()
    extra["adults"] = 0
    extra["children"] = 0
    extra["babies"] = 0
    out = clean_frame(pd.concat([sample_df, extra], ignore_index=True), drop_duplicates=False)
    assert len(out) == 5


def test_clean_generic_sales(sales_df):
    out = clean_frame(sales_df)
    assert len(out) == 5
    assert list(out.columns) == list(sales_df.columns)


def test_load_buffer_sales():
    buf = StringIO("region,units\nWest,3\nEast,8\n")
    df = load_csv_buffer(buf, filename="tiny.csv")
    assert len(df) == 2
    assert df.attrs["source_name"] == "tiny.csv"


def test_default_hotel_shape():
    df = load_default()
    assert len(df) == 87230
    assert "is_canceled" in df.columns
    assert df["arrival_date_year"].min() == 2015
    assert df["arrival_date_year"].max() == 2017
