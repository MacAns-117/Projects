-- Social Buzz popularity ranking
-- Load cleaned_reactions.csv into a table named reactions, then run this.
-- Popularity = SUM(score), not COUNT(*).

-- SQLite example (from the project root):
--   sqlite3 data/social_buzz.db
--   .mode csv
--   .import data/cleaned_reactions.csv reactions_raw

-- Clean quoted / mixed-case category labels, then rank.

WITH cleaned AS (
    SELECT
        Content_ID,
        User_ID,
        Type AS reaction,
        Datetime,
        Content_Type,
        lower(trim(replace(Content_Category, '"', ''))) AS category,
        Sentiment,
        Reaction_Score AS score
    FROM reactions
)
SELECT
    category,
    SUM(score) AS popularity_score,
    COUNT(*) AS reactions,
    ROUND(AVG(score), 2) AS mean_score,
    ROUND(100.0 * SUM(score) / (SELECT SUM(score) FROM cleaned), 2) AS share_pct
FROM cleaned
GROUP BY category
ORDER BY popularity_score DESC;

-- Top 5 only
-- SELECT * FROM (the query above) LIMIT 5;

-- Monthly volume
-- SELECT substr(Datetime, 7, 4) || '-' || substr(Datetime, 4, 2) AS year_month,
--        COUNT(*) AS reactions
-- FROM reactions
-- GROUP BY 1
-- ORDER BY 1;
