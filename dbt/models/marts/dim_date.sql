with source_dates as (

    select distinct
        period_date
    from {{ ref('stg_stats_nz_selected_price_indexes') }}
    where period_date is not null

),

dim_date as (

    select
        to_number(to_char(period_date, 'YYYYMMDD')) as date_key,
        period_date as date,
        year(period_date) as year,
        month(period_date) as month,
        to_char(period_date, 'MMMM') as month_name,
        to_char(period_date, 'YYYY-MM') as year_month

    from source_dates

)

select
    date_key,
    date,
    year,
    month,
    month_name,
    year_month
from dim_date