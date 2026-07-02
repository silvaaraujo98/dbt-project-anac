with stg_movements AS (
    select * from {{ ref('stg_movements') }}
),

stg_dim_airports_brazil AS (
    select * from {{ ref('stg_dim_airports_brazil') }}
),

stg_dim_aircrafts AS (
    select * from {{ ref('stg_dim_aircrafts') }})

select * from stg_movements left join stg_dim_airports_brazil on stg_movements.airport_reference_code = stg_dim_airports_brazil.icao_code_airport
left join stg_dim_aircrafts on stg_movements.aircraft_registration = stg_dim_aircrafts.icao_code_aircraft
