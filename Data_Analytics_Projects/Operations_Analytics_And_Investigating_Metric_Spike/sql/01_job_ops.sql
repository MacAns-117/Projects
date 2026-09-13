-- Case study 1 — job review ops
-- Load:  sqlite3 data/ops.db
--        .mode csv
--        .headers on
--        .import data/job_data.csv job_data
--
-- job_data has 8 real rows (25–30 Nov 2020). Empty Excel rows were dropped.

-- A. Jobs reviewed per hour per day (November 2020)
--    There is no time-of-day in this file, only a date.
--    Per-hour = jobs that day / 24.
SELECT
    ds,
    COUNT(*) AS jobs_reviewed,
    ROUND(COUNT(*) * 1.0 / 24, 4) AS jobs_per_hour
FROM job_data
WHERE ds BETWEEN '2020-11-01' AND '2020-11-30'
GROUP BY ds
ORDER BY ds;

-- B. Throughput = events per second that day, plus a 7-day rolling average.
--    Prefer the rolling number: daily jumps 1 vs 2 jobs on a sample this small.
--    A true 7-day window needs 7 dates; we only have 6, so this is a running mean.
WITH daily AS (
    SELECT ds, COUNT(*) AS events
    FROM job_data
    GROUP BY ds
)
SELECT
    ds,
    events,
    ROUND(events * 1.0 / 86400, 8) AS throughput,
    ROUND(
        AVG(events * 1.0 / 86400) OVER (
            ORDER BY ds
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        8
    ) AS throughput_7d
FROM daily
ORDER BY ds;

-- C. Language share, last 30 days (here: the whole file)
SELECT
    language,
    COUNT(*) AS n,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM job_data), 1) AS share_pct
FROM job_data
WHERE ds >= DATE((SELECT MAX(ds) FROM job_data), '-29 days')
GROUP BY language
ORDER BY n DESC;

-- D. Duplicate rows (every column the same)
SELECT ds, job_id, actor_id, event, language, time_spent, org, COUNT(*) AS copies
FROM job_data
GROUP BY ds, job_id, actor_id, event, language, time_spent, org
HAVING COUNT(*) > 1;

-- D2. Same job_id, different actors / events (not a full-row duplicate)
SELECT job_id, COUNT(*) AS n, COUNT(DISTINCT actor_id) AS actors
FROM job_data
GROUP BY job_id
HAVING COUNT(*) > 1;
