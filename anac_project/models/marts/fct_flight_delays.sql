select
    movement_type_code,
    flight_number,
    type_operation,
    airport_takeoff_usual_name,
    airport_takeoff_localization,
    scheduled_at_ts,
    actual_chocks_at_ts,
    actual_touch_at_ts,
    case
        when scheduled_at_ts < actual_chocks_at_ts then true
        else false
    end
        as is_delayed
    from 
        {{ ref('int_movements') }}