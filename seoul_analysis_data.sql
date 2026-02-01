-- 1. Drop the table if it already exists
DROP TABLE IF EXISTS seoul_analysis_data;

-- 2. Create a refined table for analysis
CREATE TABLE seoul_analysis_data AS
SELECT 
    자치구명,
    법정동명, 
    건물명, 
    건물용도,
    
    -- Extract year, month, day from '계약일' (e.g., '20260126' -> '2026', '01', '26')
    SUBSTR(CAST(계약일 AS TEXT), 1, 4) AS deal_year,
    SUBSTR(CAST(계약일 AS TEXT), 5, 2) AS deal_month,
    SUBSTR(CAST(계약일 AS TEXT), 7, 2) AS deal_day,
    
    -- Basic price and area info (Note: added missing commas here)
    "물건금액(만원)" AS price,
    "건물면적(㎡)" AS area,
    
    -- Calculate price per pyung (3.3m^2)
    ROUND(("물건금액(만원)" / "건물면적(㎡)" * 3.3), 2) AS price_per_pyung,
    
    -- Calculate building age at the time of contract
    SUBSTR(CAST(계약일 AS TEXT), 1, 4) - 건축년도 AS building_age,
    
    -- Group floors into Low, Middle, High categories
    CASE
        WHEN 층 <= 5 THEN 'Low'
        WHEN 층 > 5 AND 층 <= 15 THEN 'Middle'
        ELSE 'High'
    END AS floor_group,
    
    -- Define if the building is new (less than or equal to 5 years old)
    CASE
        WHEN (SUBSTR(CAST(계약일 AS TEXT), 1, 4) - 건축년도) <= 5 THEN 'New' 
        ELSE 'Old'
    END AS is_new_building
    
FROM "서울시_부동산_실거래가_정보"
WHERE "건물면적(㎡)" > 0
  AND "물건금액(만원)" > 0
  AND 건축년도 IS NOT NULL;