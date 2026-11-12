SELECT
    a.asset_id,
    a.asset_type,
    a.install_date,
    a.condition_rating,
    r.region_name,
    r.state_code
FROM {{ ref('stg_assets') }} a
LEFT JOIN {{ ref('stg_regions') }} r ON a.region_id = r.region_id
