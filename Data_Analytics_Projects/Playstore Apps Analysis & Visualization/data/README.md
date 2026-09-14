# Data

| File | Rows | Notes |
| --- | ---: | --- |
| `playstore_apps.csv` | 9,648 | One row per app. Junk category `1.9` dropped, duplicate app names dropped (keep first). **1,458 ratings left as missing** — they had been filled with the column mean (~4.19). |
| `playstore_reviews.csv` | 29,692 | Duplicate review rows dropped (37,427 → 29,692). |

Snake_case headers so SQLite does not need quoted spaces.

`installs` is the bucket floor (10,000 means “10,000+”). Revenue = `price * installs` is a **ceiling-ish estimate**, not Google’s take.
