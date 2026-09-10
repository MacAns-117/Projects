# Data

`train.csv` is the training split of:

House Price Prediction Challenge — Anmol Kumar, on Kaggle.
https://www.kaggle.com/datasets/anmolkumar/house-price-prediction-challenge

Originally collected for a MachineHack hackathon (credited to Devrup
Banerjee). 29,451 rows, 12 columns. Target:
`target(price_in_lacs)`.

Kaggle also ships `test.csv` (68,720 rows, 11 columns). That file has
**no price column**, so it is not in this repo.

Column names in this extract are lowercase. Same fields as the Kaggle
file (`POSTED_BY`, `SQUARE_FT`, …).

`longitude` / `latitude` in the file appear to be swapped relative to
real Indian coordinates. See the notebook.
