with source as (
    select * from {{source('anac_source','dim_service_type')}}
),

renamed_and_casted as (
    select 
        regexp_replace(service_type_code,r'[^a-zA-Z0-9]', '') as service_type_code,
        trim(application) as application,
        trim(type_operation) as type_operation,
        trim(service_type_description) as service_type_description
    from source
)

select * from renamed_and_casted