-- Business Question:
-- Which products experienced the largest month-over-month price increases?

with monthly_prices as (

    select
        d.date,
        p.product_key,
        p.product_name,
        f.price
    from ANALYTICS.fact_product_price f
    join ANALYTICS.dim_date d
        on f.date_key = d.date_key
    join ANALYTICS.dim_product p
        on f.product_key = p.product_key
),

price_changes as (

    select
        date,
        product_key,
        product_name,
        price,
        lag(price) over (
            partition by product_key
            order by date
        ) as previous_price
    from monthly_prices
)

select
    date,
    product_name,
    price,
    previous_price,
    round(price - previous_price, 2) as price_change
from price_changes
where previous_price is not null
order by price_change desc
limit 20;