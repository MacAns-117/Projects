# Data Analytics Projects

[![projects](https://img.shields.io/badge/projects-5-blue?style=flat-square)](.)
[![python](https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)](.)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](.)
[![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=sqlite&logoColor=white)](.)
[![Excel](https://img.shields.io/badge/Excel-217346?style=flat-square&logo=microsoft-excel&logoColor=white)](.)
[![license](https://img.shields.io/badge/license-MIT-green?style=flat-square)](.)

> Five practice analytics write-ups — pandas + SQLite on every one, Excel where a formula actually helps, a short deck each. These are assignment samples, not live warehouses.

---

## What's in here

| Folder | What it is | Headline |
| --- | --- | --- |
| [`Accenture_Data_analytics_and_Visualization`](Accenture_Data_analytics_and_Visualization/) | Social Buzz — top content categories | Animals **68,624** score; top 5 hold **36.0%** |
| [`Playstore Apps Analysis & Visualization`](Playstore%20Apps%20Analysis%20%26%20Visualization/) | Google Play — 14 SQL questions | **9,648** apps; GAME **13.9B** installs (bucket floors) |
| [`Operations_Analytics_And_Investigating_Metric_Spike`](Operations_Analytics_And_Investigating_Metric_Spike/) | Job ops + Aug 2014 engagement drop | Peak **1,443** engaged; week of 4 Aug **−12.3%** |
| [`IMDB_Movie_Analysis`](IMDB_Movie_Analysis/) | What is tied to a high IMDb score? | Genre / runtime / director; budget→gross **r = 0.63** |
| [`Cosmetics_Ingredient_Analysis`](Cosmetics_Ingredient_Analysis/) | Sephora formulas, t-SNE + cosine | Laneige cushion **$22** cheaper than AmorePacific, cosine **0.535** |

Each folder has its own README with the full tables, SQL, notebook, and deck.

---

## Social Buzz — content popularity

Accenture / Forage virtual experience. Popularity is the **sum of reaction scores**, not the count. A “super love” is 75; “disgust” is 0.

After stripping quote marks off labels: **16** categories, **22,534** reactions, **962** posts, total score **893,482**. Window 18 Jun 2020 – 18 Jun 2021.

| Rank | Category | Score | Share |
| ---: | --- | ---: | ---: |
| 1 | Animals | 68,624 | 7.7% |
| 2 | Science | 65,405 | 7.3% |
| 3 | Healthy eating | 63,138 | 7.1% |
| 4 | Technology | 63,035 | 7.1% |
| 5 | Food | 61,598 | 6.9% |

Mean score per reaction is almost flat (about 38–41), so the ranking is mostly **volume**. Same order in pandas and SQLite.

---

## Play Store — 14 SQL questions

Kaggle dump. Dropped the broken `Category = 1.9` row and duplicate app names. **9,648** apps. **Did not fill** 1,458 missing ratings.

- Highest rating is **5.0** (**271** apps). Most of those have almost no reviews.
- Most reviews: **Facebook**, 78.2M.
- Paid “revenue” (`price × installs`): **$291.1M**. Minecraft $69.9M. That is not Google’s take.
- Category with most installs: **GAME**, **13.88B** — those numbers are **bucket floors** (`10,000` means 10,000+).
- **8,895** free / **753** paid.

Sentiment scores on the review table are pre-shipped by Kaggle, not computed here.

---

## Ops analytics — the August drop

Two cases. Case 1 is **8 jobs on 6 days** (25–30 Nov 2020). There is no time of day, so “per hour” is jobs / 24. I still ran the queries. I would not ship a daily throughput from that file.

Case 2 is the real one: users / events / email, **1 May – 31 Aug 2014**. 19,066 accounts, 9,381 activated. Weekly engagement = unique users with at least one `engagement` event.

| Week starting | Engaged users |
| --- | ---: |
| 28 Jul 2014 | **1,443** (peak) |
| 4 Aug 2014 | **1,266** (−12.3%) |
| 25 Aug 2014 | **1,194** (−17.3% vs peak) |

Signups keep rising through August. Returning users fall. Phone **−25%**, tablet **−35%**, computer **−9%**. Email opens hold (~35%); CTR falls **16.1% → 10.8%**. I cannot prove a mobile bug or a broken CTA from these CSVs — those are the next checks.

---

## IMDb movie analysis

Kaggle dump, **5,043 → 4,916** unique titles. Five assigned questions in pandas, SQLite, and Excel (`=CORREL` on sheet `E_correl`).

- **Genre.** Drama is the most common tag (2,532). Highest mean IMDb (≥50 tags): Documentary **7.18**. Lowest: Horror **5.80**.
- **Duration.** Mean 107 min. Pearson **r = 0.265** with score. Bins: <90 → 6.11, **>150 → 7.44**. Runtime is a proxy for prestige mix, not a lever.
- **Language.** English is 93%. Japanese 7.35 (n=17) is famous titles, not Japanese cinema.
- **Directors.** Ranked **214 names with ≥5 films**. Nolan **8.425** (8 films). A one-film 9.5 is not a director ranking.
- **Budget.** After dropping 10 FX-contaminated >$400M rows, budget vs gross **r = 0.627**. Budget vs IMDb is ~**0.04**. Avatar profit **$523.5M**.

---

## Cosmetics — similar formulas

MedTourEasy / DataCamp *Evaluating Cosmetics Ingredients*. **1,472** Sephora SKUs. Filter: moisturizers with `Dry = 1` → **190** products. One-hot ingredient matrix **190 × 2,233**. `decyl oleate` index **25**.

t-SNE is the map. **Cosine on the binary rows** is the score.

AmorePacific Color Control Cushion SPF 50+ (**$60**, rank 4.0) vs Laneige BB Cushion Hydra Radiance SPF 50 (**$38**, rank 4.3): cosine **0.535**, **23** shared ingredients. Next neighbor is only 0.333. Close points share silicones; they are not proven safer.

---

## Tech stack across all five

| Layer | Tools |
| --- | --- |
| Language | Python 3 |
| Data | pandas, NumPy |
| SQL | SQLite (`sqlite3` stdlib) — same ranking as pandas |
| Spreadsheet | Excel — IMDb `=CORREL`, cosmetics catalogue tables |
| Similarity (cosmetics) | scikit-learn t-SNE + cosine |
| Charts | matplotlib, seaborn |
| Deck | `python-pptx` |
| Notebook | Jupyter |

No Power BI in these five. No live dashboards.

---

## Layout

```text
README.md                                              this file
Accenture_Data_analytics_and_Visualization/            Social Buzz
Playstore Apps Analysis & Visualization/               14 SQL questions
Operations_Analytics_And_Investigating_Metric_Spike/   job ops + metric spike
IMDB_Movie_Analysis/                                   five IMDb questions
Cosmetics_Ingredient_Analysis/                         t-SNE + cosine
```

Open a folder and run that child’s README (`pip install -r requirements.txt`, then the notebook).

---

## Limits

- These are **course / Forage / Kaggle samples**. Social Buzz is not the live warehouse. Play Store installs are buckets. IMDb foreign-language means are famous titles.
- I do **not** fill missing ratings, budget, or gross with the column mean.
- Ops Case 1 is too small to trust as a daily rate. The August drop is a pattern, not a root cause.
- Cosmetics t-SNE axes have no units. Use cosine if you actually want a neighbor.

---

## License

Code is MIT unless a child README says otherwise. Datasets stay with their original programmes (Forage Accenture, Kaggle, MedTourEasy / DataCamp).
