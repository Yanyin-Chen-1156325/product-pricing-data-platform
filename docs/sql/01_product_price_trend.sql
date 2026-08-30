-- Business Question:
-- How has the price of Oranges, 1kg changed over time?

select
    d.date,
    d.year_month,
    p.product_name,
    f.price,
    f.status,
    f.units
from ANALYTICS.fact_product_price f
join ANALYTICS.dim_date d
    on f.date_key = d.date_key
join ANALYTICS.dim_product p
    on f.product_key = p.product_key
where p.product_name = 'Oranges, 1kg'
order by d.date;