with stg_movements AS (
    select * from {{ ref('stg_movements') }}
),

stg_dim_airports_brazil AS (
    select * from {{ ref('stg_dim_airports_brazil') }}
),

stg_dim_service_type AS (
    select * from {{ ref('stg_dim_service_type') }}
)

select 
    a.*,
    b.usual_name,
    b.oficial_name,
    b.localization,
    c.application,
    c.type_operation,
    c.service_type_description
from 
    stg_movements as a
left join 
    stg_dim_airports_brazil as b
    on a.airport_reference_code = b.icao_code_airport
left join
    stg_dim_service_type as c
    on a.service_type_code = c.service_type_code

