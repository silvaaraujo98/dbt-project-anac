with source as (
    select * from {{ source('anac_source', 'dim_airports_brazil_icao') }}
    ),

renamed_and_casted as (
    select 
        Aeroporto as airport,
        `Nome Usual` as usual_name,
        `Nome Oficial` as oficial_name,
        `Código ICAO` as icao_code_airport,
        `Código IATA` as iata_code_airport,
        `Localização` as localization
    FROM source
)

select * from renamed_and_casted