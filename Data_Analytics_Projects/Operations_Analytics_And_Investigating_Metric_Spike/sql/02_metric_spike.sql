-- Case study 2 — investigating the engagement drop
-- Weeks start Monday.
--
-- Load (from project root):
--   sqlite3 data/ops.db
--   .mode csv
--   .headers on
--   .import data/users.csv users
--   .import data/events.csv events
--   .import data/email_events.csv email_events

-- Helper: Monday of the week for a timestamp
--   DATE(ts, '-' || ((CAST(strftime('%w', ts) AS INT) + 6) % 7) || ' days')

-- A. Weekly user engagement
--    Unique users with at least one engagement event (not signup_flow).
SELECT
    DATE(occurred_at, '-' || ((CAST(strftime('%w', occurred_at) AS INT) + 6) % 7) || ' days') AS week,
    COUNT(DISTINCT user_id) AS engaged_users,
    COUNT(*) AS events
FROM events
WHERE event_type = 'engagement'
GROUP BY 1
ORDER BY 1;

-- B. User growth — weekly signups and activations, plus running totals
WITH created AS (
    SELECT
        DATE(created_at, '-' || ((CAST(strftime('%w', created_at) AS INT) + 6) % 7) || ' days') AS week,
        COUNT(*) AS new_created
    FROM users
    GROUP BY 1
),
activated AS (
    SELECT
        DATE(activated_at, '-' || ((CAST(strftime('%w', activated_at) AS INT) + 6) % 7) || ' days') AS week,
        COUNT(*) AS new_activated
    FROM users
    WHERE activated_at IS NOT NULL AND TRIM(activated_at) != ''
    GROUP BY 1
)
SELECT
    c.week,
    c.new_created,
    COALESCE(a.new_activated, 0) AS new_activated,
    SUM(c.new_created) OVER (ORDER BY c.week) AS cum_created,
    SUM(COALESCE(a.new_activated, 0)) OVER (ORDER BY c.week) AS cum_activated
FROM created c
LEFT JOIN activated a ON a.week = c.week
ORDER BY c.week;

-- C. Weekly retention of the signup cohort (users created May–Aug 2014)
--    Age 0 = signup week. Denominator = cohort size, including pending users.
WITH cohorts AS (
    SELECT
        CAST(user_id AS INT) AS user_id,
        DATE(created_at, '-' || ((CAST(strftime('%w', created_at) AS INT) + 6) % 7) || ' days') AS created_week
    FROM users
    WHERE created_at >= '2014-05-01' AND created_at < '2014-09-01'
),
user_weeks AS (
    SELECT DISTINCT
        CAST(user_id AS INT) AS user_id,
        DATE(occurred_at, '-' || ((CAST(strftime('%w', occurred_at) AS INT) + 6) % 7) || ' days') AS week
    FROM events
    WHERE event_type = 'engagement'
),
ages AS (
    SELECT
        c.created_week,
        CAST((JULIANDAY(u.week) - JULIANDAY(c.created_week)) / 7 AS INT) AS age,
        u.user_id
    FROM user_weeks u
    JOIN cohorts c ON c.user_id = u.user_id
    WHERE u.week >= c.created_week
),
sizes AS (
    SELECT created_week, COUNT(*) AS cohort_size
    FROM cohorts
    GROUP BY 1
)
SELECT
    a.created_week,
    a.age,
    s.cohort_size,
    COUNT(DISTINCT a.user_id) AS retained,
    ROUND(100.0 * COUNT(DISTINCT a.user_id) / s.cohort_size, 1) AS retained_pct
FROM ages a
JOIN sizes s ON s.created_week = a.created_week
WHERE a.age BETWEEN 0 AND 8
GROUP BY 1, 2, 3
ORDER BY 1, 2;

-- D. Weekly engagement per device family
SELECT
    DATE(occurred_at, '-' || ((CAST(strftime('%w', occurred_at) AS INT) + 6) % 7) || ' days') AS week,
    CASE
        WHEN device IN (
            'iphone 4s','iphone 5','iphone 5s','nexus 5','samsung galaxy s4',
            'samsung galaxy note','nokia lumia 635','htc one','amazon fire phone'
        ) THEN 'phone'
        WHEN device IN (
            'ipad mini','ipad air','nexus 7','nexus 10','kindle fire',
            'windows surface','samsumg galaxy tablet'
        ) THEN 'tablet'
        ELSE 'computer'
    END AS device_family,
    COUNT(DISTINCT user_id) AS engaged_users
FROM events
WHERE event_type = 'engagement'
GROUP BY 1, 2
ORDER BY 1, 2;

-- E. Email engagement
--    Open rate  = opens / (digest + reengagement sends)
--    CTR        = clickthroughs / sends
--    Click-to-open = clickthroughs / opens
SELECT
    DATE(occurred_at, '-' || ((CAST(strftime('%w', occurred_at) AS INT) + 6) % 7) || ' days') AS week,
    SUM(action = 'sent_weekly_digest') AS digest_sent,
    SUM(action = 'sent_reengagement_email') AS reengagement_sent,
    SUM(action = 'email_open') AS opens,
    SUM(action = 'email_clickthrough') AS clicks,
    ROUND(
        100.0 * SUM(action = 'email_open')
        / NULLIF(SUM(action IN ('sent_weekly_digest','sent_reengagement_email')), 0)
    , 1) AS open_rate_pct,
    ROUND(
        100.0 * SUM(action = 'email_clickthrough')
        / NULLIF(SUM(action IN ('sent_weekly_digest','sent_reengagement_email')), 0)
    , 1) AS ctr_pct
FROM email_events
GROUP BY 1
ORDER BY 1;
