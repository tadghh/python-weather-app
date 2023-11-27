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
       AVG(min_temp) AS avg_min_temp,
       AVG(max_temp) AS avg_max_temp,
       AVG(avg_temp) AS avg_mean_temp
FROM weather
WHERE NOT (
        (min_temp LIKE '%M%' OR min_temp IS null) 
        AND (max_temp LIKE '%M%' OR max_temp IS null) 
        AND (avg_temp LIKE '%M%' OR avg_temp IS null)
    )
GROUP BY month
ORDER BY month;

-- Select used in fetch_data (returns null instead of 'M')
SELECT sample_date,
    CASE 
        WHEN min_temp LIKE '%M%' THEN NULL
        ELSE min_temp
    END AS min_temp,
    CASE 
        WHEN max_temp LIKE '%M%' THEN NULL
        ELSE max_temp
    END AS max_temp,
    CASE 
        WHEN avg_temp LIKE '%M%' THEN NULL
        ELSE avg_temp
    END AS avg_temp
FROM 
    weather
WHERE 
    strftime('%Y', sample_date) BETWEEN '1996' AND '2000'
	 AND NOT (
        (min_temp LIKE '%M%' OR min_temp IS null) 
        AND (max_temp LIKE '%M%' OR max_temp IS null) 
        AND (avg_temp LIKE '%M%' OR avg_temp IS null)
    );
