select
    year_flight,
    month_flight,
    airport_takeoff_localization,
    count(movement_id) as total_flights,
    sum(total_passengers_handled) as total_passengers_handled
from
    {{ ref('fct_flight_movement') }}
group by all