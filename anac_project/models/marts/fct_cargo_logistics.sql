select
    movement_type_code,
    flight_number,
    type_operation,
    airport_takeoff_usual_name,
    airport_localization_name,
    month_flight,
    year_flight,
    scheduled_at_ts,
    actual_chocks_at_ts,
    actual_touch_at_ts,
    mail_kg,
    cargo_kg,
    mail_kg + cargo_kg as total_weight
from
    {{ ref('int_movements') }}
where mail_kg is not null and cargo_kg is not null
order by total_weight desc