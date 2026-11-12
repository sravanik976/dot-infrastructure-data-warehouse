SELECT 
    asset_id, 
    asset_type, 
    region_id, 
    install_date, 
    condition_rating
FROM {{ source('dot_raw', 'assets') }}
