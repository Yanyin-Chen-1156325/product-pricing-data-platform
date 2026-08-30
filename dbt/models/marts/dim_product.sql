with products as (

    select distinct
        series_reference,
        series_title_1 as product_name

    from {{ ref('stg_stats_nz_selected_price_indexes') }}

    where units = 'Dollars'
      and series_reference is not null
      and series_title_1 is not null

),

dim_product as (

    select
        row_number() over (
            order by series_reference
        ) as product_key,
        series_reference,
        product_name

    from products

)

select
    product_key,
    series_reference,
    product_name

from dim_product