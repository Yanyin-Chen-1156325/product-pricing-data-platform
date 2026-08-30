-- Business Question:
-- How has the selected price index changed over time?

select
    d.date,
    d.year_month,
    f.series_reference,
    f.index_value,
    f.status,
    f.units
from ANALYTICS.fact_price_index f
join ANALYTICS.dim_date d
    on f.date_key = d.date_key
where f.series_reference = 'CPIM.SE901'
order by d.date;