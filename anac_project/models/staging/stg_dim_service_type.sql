with source as (
    select * from {{source('anac_source','dim_servicetype')}}
),

renamed_and_casted as (
    select 
        trim(service_type_code) as service_type_code,
        trim(application) as application,
        trim(type_operation) as type_operation,
        trim(service_type_description) as service_type_description
    from source
)

select * from renamed_and_casted