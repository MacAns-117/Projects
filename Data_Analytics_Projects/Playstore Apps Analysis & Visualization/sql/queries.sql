-- Play Store module 1 — 14 questions
-- sqlite3 data/playstore.db
-- .mode csv
-- .headers on
-- .import data/playstore_apps.csv apps
-- .import data/playstore_reviews.csv reviews

-- Q1. Apps with the highest rating
SELECT app, rating
FROM apps
WHERE rating = (SELECT MAX(rating) FROM apps)
ORDER BY app;

-- Q2. Installs and reviews for those apps, highest reviews first
SELECT app, installs, reviews, rating
FROM apps
WHERE rating = (SELECT MAX(rating) FROM apps)
ORDER BY reviews DESC;

-- Q3. App with the highest number of reviews
SELECT app, category, reviews
FROM apps
ORDER BY reviews DESC
LIMIT 1;

-- Q4. Revenue from paid apps (list price × install bucket — not actual receipts)
SELECT ROUND(SUM(price * installs), 2) AS total_revenue
FROM apps
WHERE type = 'Paid';

-- Q5. Category with the most installs
SELECT category, SUM(installs) AS total_installs
FROM apps
GROUP BY category
ORDER BY total_installs DESC
LIMIT 1;

-- Q6. Genre with the most published apps
SELECT genres, COUNT(*) AS published_apps
FROM apps
GROUP BY genres
ORDER BY published_apps DESC
LIMIT 1;

-- Q7. Games by installs (distinct app names)
SELECT DISTINCT app, installs
FROM apps
WHERE category = 'GAME'
ORDER BY installs DESC;

-- Q8. Apps that list Android 4.0.3 and up
SELECT app, android_ver
FROM apps
WHERE android_ver = '4.0.3 and up';

-- Q9. Free vs paid counts
SELECT type, COUNT(*) AS n
FROM apps
GROUP BY type;

-- Q10. Dating app with the most reviews
SELECT app AS best_dating_app, reviews, rating, installs
FROM apps
WHERE category = 'DATING'
ORDER BY reviews DESC
LIMIT 1;

-- Q11. Sentiment split for "10 Best Foods for You"
SELECT sentiment, COUNT(*) AS n
FROM reviews
WHERE app = '10 Best Foods for You'
GROUP BY sentiment;

-- Q12. ASUS SuperNote comments with polarity = 1 and subjectivity = 1
SELECT app, translated_review
FROM reviews
WHERE app = 'ASUS SuperNote'
  AND sentiment_polarity = 1
  AND sentiment_subjectivity = 1;

-- Q13. Neutral reviews for Abs Training-Burn belly fat
SELECT app, translated_review, sentiment
FROM reviews
WHERE app = 'Abs Training-Burn belly fat'
  AND sentiment = 'Neutral';

-- Q14. Negative reviews for Adobe Acrobat Reader
SELECT app, translated_review, sentiment, sentiment_polarity, sentiment_subjectivity
FROM reviews
WHERE app = 'Adobe Acrobat Reader'
  AND sentiment = 'Negative';
