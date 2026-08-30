with product_prices as (

    select
        series_reference,
        period_date,
        data_value,
        status,
        units

    from {{ ref('stg_stats_nz_selected_price_indexes') }}

    where units = 'Dollars'
      and series_reference is not null
      and period_date is not null
      and data_value is not null

),

fact_product_price as (

    select
        d.date_key,
        p.product_key,
        pp.data_value as price,
        pp.status,
        pp.units

    from product_prices pp

    inner join {{ ref('dim_product') }} p
        on pp.series_reference = p.series_reference

    inner join {{ ref('dim_date') }} d
        on pp.period_date = d.date

)

select
    date_key,
    product_key,
    price,
    status,
    units

from fact_product_price