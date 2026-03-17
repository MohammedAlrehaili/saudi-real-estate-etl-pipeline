SELECT 
    city,
    district,
    -- حساب متوسط نقاط الفخامة في الحي
    -- كلما زاد الرقم، زادت الرفاهية في ذلك الحي
    ROUND(AVG(
        pool + 
        elevator + 
        fireplace + 
        garage + 
        driver_room + 
        maid_room + 
        furnished
    ), 2) AS luxury_index,
    
    -- حساب متوسط عدد غرف النوم
    ROUND(AVG(bedrooms), 1) AS avg_bedrooms,
    
    -- حساب متوسط السعر للتأكد من ربط الفخامة بالقيمة
    ROUND(AVG(price), 0) AS avg_price,
    
    -- عدد العقارات في الحي
    COUNT(*) AS total_properties
FROM 
    `saudi-real-estate-project.saudi_real_estate_data.houses_table`
GROUP BY 
    city, district
HAVING 
    total_properties > 5 -- استبعاد الأحياء ذات البيانات القليلة
ORDER BY 
    luxury_index DESC, -- الأولوية للأحياء الأكثر رفاهية
    avg_bedrooms DESC
LIMIT 10;