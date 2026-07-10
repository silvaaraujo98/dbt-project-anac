with source as (
    select * from {{ source('anac_source', 'dim_airports_brazil_icao') }}
    ),

renamed_and_casted as (
    select 
        Aeroporto as airport,
        trim(`Nome Usual`) as usual_name,
        trim(`Nome Oficial`) as oficial_name,
        trim(`Código ICAO`) as icao_code_airport,
        trim(`Código IATA`) as iata_code_airport,
        trim(`Localização`) as localization
    FROM source
)

select * from renamed_and_casted