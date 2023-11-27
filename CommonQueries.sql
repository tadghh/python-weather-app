-- Get all data
SELECT * FROM weather ORDER BY sample_date ASC

-- Calculate average for mean
SELECT strftime('%m', sample_date) AS month,
       ROUND(AVG(avg_temp), 2) AS avg_min_temp
FROM weather
GROUP BY month
ORDER BY month;

-- Calculate average for min
SELECT strftime('%m', sample_date) AS month,
       ROUND(AVG(min_temp), 2) AS avg_min_temp
FROM weather
GROUP BY month
ORDER BY month;

-- Calculate average for max
SELECT strftime('%m', sample_date) AS month,
       ROUND(AVG(max_temp), 2) AS avg_max_temp
FROM weather
GROUP BY month
ORDER BY month;

-- Calculate average for all months for min, max, and mean
SELECT strftime('%m', sample_date) AS month,
       ROUND(AVG(min_temp), 2) AS avg_min_temp,
       ROUND(AVG(max_temp), 2) AS avg_max_temp,
       ROUND(AVG(avg_temp), 2) AS avg_mean_temp
FROM weather
GROUP BY month
ORDER BY month;
