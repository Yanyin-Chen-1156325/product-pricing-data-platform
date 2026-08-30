with price_indexes as (

    select
        series_reference,
        period_date,
        data_value,
        status,
        units

    from {{ ref('stg_stats_nz_selected_price_indexes') }}

    where units = 'Index'
      and series_reference is not null
      and period_date is not null
      and data_value is not null

),

fact_price_index as (

    select
        d.date_key,
        pi.series_reference,
        pi.data_value as index_value,
        pi.status,
        pi.units

    from price_indexes pi

    inner join {{ ref('dim_date') }} d
        on pi.period_date = d.date

)

select
    date_key,
    series_reference,
    index_value,
    status,
    units

from fact_price_index