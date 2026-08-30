select
    product_key,
    date_key,
    count(*) as row_count
from {{ ref('fact_product_price') }}
group by
    product_key,
    date_key
having count(*) > 1