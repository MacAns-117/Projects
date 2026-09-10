"""Streamlit app for the Indian house price model.

Uses the same features as notebooks/house_price_prediction.ipynb:
area, BHK, city, who posted it, RERA, resale, under construction.
Does not take ₹/sqft — that number is the price.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "gradient_boosting.joblib"

NUMERIC = ["log_sqft", "bhk", "rera", "under_construction", "resale", "is_metro"]
CATEGORICAL = ["posted_by", "city_group"]


@st.cache_resource
def load_bundle():
    if not MODEL_PATH.exists():
        return None
    bundle = joblib.load(MODEL_PATH)
    if isinstance(bundle, dict) and "model" in bundle:
        return bundle
    return {
        "model": bundle,
        "keep_cities": [],
        "metros": [],
        "numeric": NUMERIC,
        "categorical": CATEGORICAL,
    }


def features_from_inputs(posted_by, city, square_ft, bhk, rera, under_construction, resale, keep_cities, metros):
    city_group = city if city in keep_cities else "Other"
    row = {
        "log_sqft": float(np.log1p(square_ft)),
        "bhk": int(min(bhk, 6)),
        "rera": int(rera),
        "under_construction": int(under_construction),
        "resale": int(resale),
        "is_metro": int(city in metros),
        "posted_by": posted_by,
        "city_group": city_group,
    }
    return pd.DataFrame([row], columns=NUMERIC + CATEGORICAL)


def main():
    st.set_page_config(page_title="Indian house price", layout="centered")
    st.title("Indian house price predictor")
    st.write(
        "Guesses an asking price from size, city, BHK, and a few listing flags. "
        "Holdout median error is about **₹12 lakh**; treat it as a ballpark, not a valuation."
    )

    bundle = load_bundle()
    if bundle is None:
        st.error(
            "Missing `models/gradient_boosting.joblib`. "
            "Run `notebooks/house_price_prediction.ipynb` first."
        )
        return

    model = bundle["model"]
    keep_cities = list(bundle.get("keep_cities") or [])
    metros = set(bundle.get("metros") or [])
    city_options = keep_cities + (["Other"] if "Other" not in keep_cities else [])

    posted_by = st.selectbox("Posted by", ["Dealer", "Owner", "Builder"])
    city = st.selectbox("City", city_options, index=city_options.index("Bangalore") if "Bangalore" in city_options else 0)
    square_ft = st.number_input("Area (sq ft)", min_value=200, max_value=8000, value=1170, step=10)
    bhk = st.selectbox("BHK", [1, 2, 3, 4, 5, 6], index=1)
    rera = st.selectbox("RERA approved", ["No", "Yes"])
    status = st.selectbox("Status", ["Ready to move", "Under construction"])
    resale = st.selectbox("Resale", ["Yes", "No"])

    if city in ("Lalitpur", "Maharashtra"):
        st.caption(
            "A lot of listings tagged Lalitpur / Maharashtra are actually Mumbai-region "
            "(Thane, Mulund, Chembur). The model treats that label as a Mumbai-ish bucket."
        )

    if st.button("Predict"):
        X = features_from_inputs(
            posted_by=posted_by,
            city=city,
            square_ft=square_ft,
            bhk=bhk,
            rera=1 if rera == "Yes" else 0,
            under_construction=1 if status == "Under construction" else 0,
            resale=1 if resale == "Yes" else 0,
            keep_cities=set(keep_cities),
            metros=metros,
        )
        price_lakh = float(np.expm1(model.predict(X)[0]))
        rupees = price_lakh * 100_000
        st.success(f"Estimated asking price: **₹{price_lakh:,.1f} lakh**  (₹{rupees:,.0f})")
        st.caption("Typical holdout error is around ₹12 lakh. Mumbai listings can miss by more.")


if __name__ == "__main__":
    main()
