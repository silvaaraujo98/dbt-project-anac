with

source as (

    select * from {{ source('anac_source', 'movements_raw') }}
    {% if target.name == 'dev' %}
    -- Assumes dt_toque is in a format that supports string comparison, or adjust to your raw column format
    where dt_toque >= '01/12/2015' and dt_toque <= '31/12/2025' 
    {% endif %}

),

renamed_and_casted as (

    select
        -- Generate a unique key for each movement
        {{ dbt_utils.generate_surrogate_key([
            'NR_AEROPORTO_REFERENCIA', 
            'DT_PREVISTO', 
            'HH_PREVISTO', 
            'NR_VOO_NUMERO', 
            'NR_AERONAVE_MARCAS'
        ]) }} as movement_id,

        -- IDs and Codes
        nr_aeroporto_referencia as airport_reference_code,
        nr_movimento_tipo as movement_type_code,
        nr_aeronave_operador as aircraft_operator_code,
        nr_aeronave_marcas as aircraft_registration,
        nr_aeronave_tipo as aircraft_type_code,
        nr_voo_outro_aeroporto as other_airport_code,
        nr_voo_numero as flight_number,
        nr_service_type as service_type_code,
        nr_natureza as flight_nature_code,
        nr_cabeceira as runway_code,
        nr_box as parking_bay_code,
        nr_ponte_conector_remoto as gate_code,
        nr_terminal as terminal_code,

        -- Timestamps (combining date and time and casting to TIMESTAMP)
        safe_cast(
            parse_timestamp('%Y-%m-%d %H:%M:%S', dt_previsto || ' ' || hh_previsto) as timestamp
        ) as scheduled_at_ts,
        safe_cast(
            parse_timestamp('%Y-%m-%d %H:%M:%S', dt_calco || ' ' || hh_calco) as timestamp
        ) as actual_chocks_at_ts,
        safe_cast(
            parse_timestamp('%Y-%m-%d %H:%M:%S', dt_toque || ' ' || hh_toque) as timestamp
        ) as actual_touch_at_ts,

        -- Quantities (casting to INTEGER, handling NULLs)
        safe_cast(qt_pax_local as integer) as local_passengers_quantity,
        safe_cast(qt_pax_conexao_domestico as integer) as domestic_connecting_passengers_quantity,
        safe_cast(qt_pax_conexao_internacional as integer) as international_connecting_passengers_quantity,

        -- Weights (casting to NUMERIC, handling NULLs)
        safe_cast(replace(qt_correio, ',', '.') as numeric) as mail_kg,
        safe_cast(replace(qt_carga, ',', '.') as numeric) as cargo_kg

    from source

)

select * from renamed_and_casted
-- Filter data for dev environment to have a faster process.