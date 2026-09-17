"""Fixtures. Hotel CSV is loaded only in tests that ask for it."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "hotel": ["City Hotel", "Resort Hotel", "City Hotel", "City Hotel", "Resort Hotel"],
            "is_canceled": [1, 0, 1, 0, 0],
            "lead_time": [80, 30, 120, 15, 45],
            "arrival_date_year": [2016, 2017, 2015, 2016, 2017],
            "arrival_date_month": ["August", "July", "November", "May", "June"],
            "adults": [2, 1, 2, 1, 2],
            "children": [0, 0, 1, 0, 0],
            "babies": [0, 0, 0, 0, 1],
            "adr": [100.0, 150.0, 80.0, 200.0, 120.0],
            "customer_type": ["Transient", "Transient", "Contract", "Transient", "Group"],
            "market_segment": ["Online TA", "Corporate", "Online TA", "Direct", "Groups"],
            "total_of_special_requests": [0, 1, 2, 0, 3],
        }
    )


@pytest.fixture
def sales_df():
    return pd.DataFrame(
        {
            "region": ["West", "West", "East", "East", "North"],
            "product": ["Widget", "Gadget", "Widget", "Gadget", "Widget"],
            "units": [10, 4, 7, 12, 3],
            "price": [12.5, 40.0, 12.5, 40.0, 12.5],
        }
    )
