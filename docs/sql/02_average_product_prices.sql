-- Business Question:
-- Which products have the highest average monthly prices?

select
    p.product_name,
    round(avg(f.price), 2) as average_price
from ANALYTICS.fact_product_price f
join ANALYTICS.dim_product p
    on f.product_key = p.product_key
group by p.product_name
order by average_price desc
limit 10;