SELECT 
    log_id, 
    asset_id, 
    work_type, 
    CAST(cost AS NUMERIC(10,2)) AS maintenance_cost, 
    completed_at
FROM {{ source('dot_raw', 'maintenance_logs') }}
