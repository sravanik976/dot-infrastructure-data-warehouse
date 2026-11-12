{{
  config(
    materialized='incremental',
    unique_key='log_id'
  )
}}

SELECT
    log_id,
    asset_id,
    work_type,
    maintenance_cost,
    completed_at
FROM {{ ref('stg_maintenance_logs') }}

{% if is_incremental() %}
  WHERE completed_at > (SELECT MAX(completed_at) FROM {{ this }})
{% endif %}
