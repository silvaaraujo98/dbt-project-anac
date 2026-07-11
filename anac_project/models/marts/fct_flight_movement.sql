--  The central fact model. It records every aircraft landing or takeoff event with granular passenger totals.
select
    movement_id,
    movement_type_code,
    flight_number,
    type_operation,
    airport_takeoff_usual_name,
    airport_takeoff_localization,
    month_flight,
    year_flight,
    scheduled_at_ts,
    actual_chocks_at_ts,
    actual_touch_at_ts,
    local_passengers_quantity +  domestic_connecting_passengers_quantity + international_connecting_passengers_quantity as total_passengers_handled,
    mail_kg,
    cargo_kg
from 
    {{ ref('int_movements') }}