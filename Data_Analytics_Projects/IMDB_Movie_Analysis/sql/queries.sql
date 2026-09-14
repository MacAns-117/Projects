-- IMDb tasks A–E (SQLite)
-- Notebook builds three tables in memory: movies, movie_genres, sane_budget.

-- A. Genre counts + IMDb stats
SELECT genre,
       COUNT(*)                  AS n,
       ROUND(AVG(imdb_score), 3) AS mean_score,
       ROUND(MIN(imdb_score), 1) AS min_score,
       ROUND(MAX(imdb_score), 1) AS max_score
FROM movie_genres
GROUP BY genre
ORDER BY n DESC;

-- B. Duration bins vs mean score
SELECT CASE
         WHEN duration < 90  THEN '<90'
         WHEN duration < 120 THEN '90-120'
         WHEN duration < 150 THEN '120-150'
         ELSE '>150'
       END AS dur_bin,
       COUNT(*)                  AS n,
       ROUND(AVG(imdb_score), 3) AS mean_score
FROM movies
WHERE duration IS NOT NULL
GROUP BY 1
ORDER BY MIN(duration);

-- C. Language
SELECT language,
       COUNT(*)                  AS n,
       ROUND(AVG(imdb_score), 3) AS mean_score
FROM movies
WHERE language IS NOT NULL
GROUP BY language
ORDER BY n DESC;

-- D. Directors with at least 5 films
SELECT director_name,
       COUNT(*)                  AS n,
       ROUND(AVG(imdb_score), 3) AS mean_score,
       ROUND(MAX(imdb_score), 1) AS best
FROM movies
WHERE director_name IS NOT NULL
GROUP BY director_name
HAVING COUNT(*) >= 5
ORDER BY mean_score DESC;

-- E. Profit = gross - budget (USD-ish rows)
SELECT movie_title, title_year, country, budget, gross,
       (gross - budget) AS profit
FROM sane_budget
ORDER BY profit DESC
LIMIT 15;
