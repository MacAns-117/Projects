# Ops analytics and the August engagement drop

Two SQL case studies from an ops-analytics assignment. I loaded the
tables, answered the questions in **pandas and SQLite**, and put the
numbers in a short deck.

This is a practice project. Case 1 is **8 rows**. I still ran every
query the brief asked for, and I say in the write-up when a metric is
too thin to trust.

## What I was asked

**Case 1 — job review ops** (`job_data`, Nov 2020)

- Jobs reviewed per hour per day
- Throughput (events per second) and a 7-day rolling average
- Language share, last 30 days
- How to show duplicate rows

**Case 2 — metric spike** (users / events / email, May–Aug 2014)

- Weekly user engagement
- User growth
- Weekly retention of the signup cohort
- Weekly engagement by device
- Email engagement

## Result (actual numbers)

### Case 1

After dropping three empty Excel rows: **8 jobs, 6 days** (25–30 Nov
2020). There is **no time of day**, so “per hour” is jobs / 24.

| Date | Jobs | Jobs / hour | Events / second |
| --- | ---: | ---: | ---: |
| 25 Nov | 1 | 0.0417 | 0.0000116 |
| 26 Nov | 1 | 0.0417 | 0.0000116 |
| 27 Nov | 1 | 0.0417 | 0.0000116 |
| 28 Nov | 2 | 0.0833 | 0.0000231 |
| 29 Nov | 1 | 0.0417 | 0.0000116 |
| 30 Nov | 2 | 0.0833 | 0.0000231 |

7-day rolling throughput (running mean, we only have 6 days): ends at
**0.0000154** events/sec. I would **not** use the daily number on a
sample this small — one extra job doubles it. Rolling is the better
habit, but it needs more days than this file has.

Language share (the whole file *is* the last 30 days): **Persian 37.5%**
(3/8), everything else 12.5% each.

Exact duplicate rows: **none**. `job_id` 23 shows up three times with
different actors / events. That is a repeated job, not a copied row.

### Case 2

Product events run **1 May – 31 Aug 2014**. 19,066 accounts, 9,381
activated (49.2%). 340,832 events, 90,389 email rows.

Weekly engagement = unique users with at least one `engagement` event.
Weeks start Monday. The week of 28 Apr is a partial week (data starts
Thursday 1 May).

| Week starting | Engaged users | Events |
| --- | ---: | ---: |
| 28 Jul 2014 | **1,443** (peak) | 21,472 |
| 4 Aug 2014 | **1,266** (−12.3%) | 18,341 |
| 25 Aug 2014 | **1,194** (−17.3% vs peak) | 16,166 |

Signups **keep rising** through August (476 → 406 → 473 → 468 → 514).
This is not an acquisition hole. Returning users fall
(1,153 → 1,055 → 943 → 908). New-to-engagement dips only in the week of
4 Aug, then recovers.

Pooled signup-cohort retention (May–Aug 2014 signups, 7,298 users):

| Weeks after signup | Still engaged |
| ---: | ---: |
| 0 | 50.4% |
| 1 | 34.1% |
| 2 | 20.3% |
| 4 | 10.2% |
| 8 | 4.8% |

Week 0 is ~50% because only activated accounts ever engage. The
denominator is **all signups**, which is what the brief asked for.

Device family, peak week vs last week (unique engaged users):

| | 28 Jul | 25 Aug | Change |
| --- | ---: | ---: | ---: |
| Computer | 951 | 864 | −9% |
| Phone | 589 | 441 | −25% |
| Tablet | 250 | 163 | −35% |

Email, whole window: **33.6% open**, **14.8% CTR**, 44% click-to-open.

| Week | Open rate | CTR |
| --- | ---: | ---: |
| 28 Jul | 35.2% | **16.1%** |
| 4 Aug | 33.4% | **10.8%** |
| 25 Aug | 35.0% | 11.3% |

Opens hold. Clicks do not. Event mix (home / like / inbox / login) is
almost the same before and after the drop, so this is not one feature
disappearing from the log.

**What I would tell ops:** growth is fine; existing users, especially on
phone and tablet, showed up less from the week of 4 Aug; digest
click-through fell at the same time. I **cannot prove** a mobile bug or
a broken email CTA from these tables. Those are the next checks, not
the conclusion.

Deck: [`reports/Ops_Analytics_Report.pptx`](reports/Ops_Analytics_Report.pptx).

## How to rerun

```bash
python -m pip install -r requirements.txt
jupyter notebook notebooks/ops_analytics.ipynb
```

The notebook writes the figures again and runs the same ranking in
SQLite (`sqlite3` is in the stdlib). SQL by itself:

- [`sql/01_job_ops.sql`](sql/01_job_ops.sql)
- [`sql/02_metric_spike.sql`](sql/02_metric_spike.sql)

Rebuild the deck with `python reports/build_pptx.py` if the numbers
change.

## Layout

```text
README.md
requirements.txt
data/job_data.csv
data/users.csv
data/events.csv
data/email_events.csv
sql/01_job_ops.sql
sql/02_metric_spike.sql
notebooks/ops_analytics.ipynb
reports/figures/*.png
reports/Ops_Analytics_Report.pptx
docs/project_brief.docx
```

| File you started with | Where it lives now |
| --- | --- |
| `SQL Project-1 Table.xlsx` | `data/job_data.xlsx` + cleaned `data/job_data.csv` |
| `Table-1 users.csv` | `data/users.csv` |
| `Table-2 events.csv` | `data/events.csv` |
| `Table-3 email_events.csv` | `data/email_events.csv` |
| `Operation_Analytics_and_Investigating_Metric-Spike_INFO.docx` | `docs/project_brief.docx` |
