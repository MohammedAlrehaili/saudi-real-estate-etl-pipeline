-- Analyzing how property age affects the average price in major cities
SELECT 
    city,
    age_category,
    ROUND(AVG(price), 0) AS avg_price,
    ROUND(AVG(price_per_meter), 2) AS avg_meter_price,
    COUNT(*) AS unit_count
FROM 
    `saudi-real-estate-project.saudi_real_estate_data.houses_table`
GROUP BY 
    city, age_category
ORDER BY 
    city, 
    avg_price DESC;