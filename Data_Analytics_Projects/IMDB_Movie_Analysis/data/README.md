# Data

| File | Rows | Notes |
| --- | ---: | --- |
| `imdb_movies.csv` | 4,916 | Unique titles. Stripped `\xa0` off titles, dropped 45 exact duplicate rows, then 82 extra title copies (kept the row with more votes). |
| `genre_imdb_stats.csv` | 26 | Exploded genre tags with mean/median/mode/range/var/std of IMDb. |

Raw dump had 5,043 rows. 105 titles have no `title_year` (mostly TV). 10 budgets above $400M are local-currency, not USD.
