-- Business Question:
-- Does the price of Oranges, 1kg move in the same direction as the selected price index?

with product_prices as (

    select
        d.date,
        f.price
    from ANALYTICS.fact_product_price f
    join ANALYTICS.dim_date d
        on f.date_key = d.date_key
    join ANALYTICS.dim_product p
        on f.product_key = p.product_key
    where p.product_name = 'Oranges, 1kg'

),

price_index as (

    select
        d.date,
        f.index_value
    from ANALYTICS.fact_price_index f
    join ANALYTICS.dim_date d
        on f.date_key = d.date_key
    where f.series_reference = 'CPIM.SE901'

),

monthly_changes as (

    select
        p.date,
        p.price,
        i.index_value,

        p.price - lag(p.price) over (
            order by p.date
        ) as price_change,

        i.index_value - lag(i.index_value) over (
            order by i.date
        ) as index_change

    from product_prices p
    join price_index i
        on p.date = i.date
)

select
    date,
    price,
    index_value,
    round(price_change, 2) as price_change,
    round(index_change, 2) as index_change
from monthly_changes
where price_change is not null
  and index_change is not null
order by date;