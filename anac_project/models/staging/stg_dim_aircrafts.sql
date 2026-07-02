with source as (
    select * from {{ source('anac_source', 'dim_aircraft') }}
    ),

renamed_and_casted as (
    select 
        `ICAO code` as icao_code_aircraft,
        `IATA type code` as iata_type_code_aircraft,
        `Model` as model
    FROM source
)

select * from renamed_and_casted