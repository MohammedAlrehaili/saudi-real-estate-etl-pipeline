-- Searching for districts where price per meter is below average but house size/rooms are high
SELECT 
    city,
    district,
    ROUND(AVG(price_per_meter), 2) AS avg_meter_price,
    ROUND(AVG(bedrooms), 1) AS avg_bedrooms,
    COUNT(*) AS total_listings
FROM 
    `saudi-real-estate-project.saudi_real_estate_data.houses_table`
GROUP BY 
    city, district
HAVING 
    total_listings > 10
ORDER BY 
    avg_meter_price ASC, 
    avg_bedrooms DESC
LIMIT 10;