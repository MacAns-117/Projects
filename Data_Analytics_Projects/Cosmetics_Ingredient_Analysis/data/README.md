# Data

| File | Rows | Notes |
| --- | ---: | --- |
| `cosmetics.csv` | 1,472 | Sephora scrape. Six `Label`s, 116 brands, ingredient lists, five skin-type flags. |
| `moisturizers_dry_tsne.csv` | 190 | Moisturizers with `Dry=1`, plus t-SNE `X`,`Y` (`random_state=42`). |
| `amorepacific_neighbors.csv` | 8 | Cosine neighbors of the AmorePacific cushion. |

120 rows have `Ingredients` like “Visit the … boutique” — leftover scrape text, not a formula. They still sit in the catalogue counts; they add almost no tokens to the DTM.
