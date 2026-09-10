# Models

`gradient_boosting.joblib` is a dict:

- `model` — sklearn pipeline (one-hot + gradient boosting on log price)
- `keep_cities` — cities with ≥ 80 listings in the cleaned table
- `metros` — names used for the `is_metro` flag
- `numeric` / `categorical` — column order the pipeline expects

The notebook writes this file. The Streamlit app (`app.py`) reads it.
