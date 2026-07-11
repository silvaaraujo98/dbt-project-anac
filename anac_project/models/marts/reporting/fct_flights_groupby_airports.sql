select
    year_flight,
    month_flight,
    airport_localization_name,
    sum(total_passengers_handled) as total_passengers_handled
from
    {{ ref('fct_flight_movement') }}
group by all