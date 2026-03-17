-- Calculating the cost of each 'Luxury Point' to find the best value-for-money districts
WITH LuxuryTable AS (
    SELECT 
        city,
        district,
        price,
        (pool + elevator + garage + driver_room + maid_room) AS luxury_points
    FROM `saudi-real-estate-project.saudi_real_estate_data.houses_table`
    WHERE (pool + elevator + garage + driver_room + maid_room) > 0
)
SELECT 
    city,
    district,
    ROUND(AVG(price / luxury_points), 0) AS cost_per_luxury_point,
    COUNT(*) AS listings
FROM LuxuryTable
GROUP BY city, district
HAVING listings > 5
ORDER BY cost_per_luxury_point ASC
LIMIT 10;