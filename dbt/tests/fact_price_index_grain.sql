select
    series_reference,
    date_key,
    count(*) as row_count
from {{ ref('fact_price_index') }}
group by
    series_reference,
    date_key
having count(*) > 1