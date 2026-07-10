with stg_movements AS (
    select * from {{ ref('stg_movements') }}
),

stg_dim_airports_brazil AS (
    select * from {{ ref('stg_dim_airports_brazil') }}
)

select 
    * 
from 
    stg_movements 
left join 
    stg_dim_airports_brazil 
    on stg_movements.airport_reference_code = stg_dim_airports_brazil.icao_code_airport
left join
    stg_dim_service_type
    on stg_movements.service_type_code = stg_dim_service_type.service_type_code

