SELECT 
    region_id, 
    TRIM(region_name) AS region_name, 
    UPPER(state_code) AS state_code
FROM {{ source('dot_raw', 'regions') }}
