-- Catalogue questions (SQLite). t-SNE stays in Python.

-- Products by category
SELECT Label, COUNT(*) AS n,
       ROUND(AVG(Price), 1) AS mean_price,
       ROUND(AVG(Rank), 2) AS mean_rank
FROM cosmetics
GROUP BY Label
ORDER BY n DESC;

-- Brands with the most SKUs
SELECT Brand, COUNT(*) AS n,
       ROUND(AVG(Price), 1) AS mean_price
FROM cosmetics
GROUP BY Brand
ORDER BY n DESC
LIMIT 15;

-- Skin-type flags (a product can tick several)
SELECT
  SUM(Combination) AS combination,
  SUM(Dry) AS dry,
  SUM(Normal) AS normal,
  SUM(Oily) AS oily,
  SUM(Sensitive) AS sensitive,
  SUM(CASE WHEN Combination+Dry+Normal+Oily+Sensitive = 0 THEN 1 ELSE 0 END) AS no_skin_flag
FROM cosmetics;

-- Dry-skin moisturizers used for the map
SELECT COUNT(*) AS n, ROUND(AVG(Price), 1) AS mean_price, ROUND(AVG(Rank), 2) AS mean_rank
FROM cosmetics
WHERE Label = 'Moisturizer' AND Dry = 1;
