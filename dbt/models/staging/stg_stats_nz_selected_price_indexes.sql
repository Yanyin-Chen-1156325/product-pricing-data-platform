select
    trim(series_reference) as series_reference,

    to_date(
        concat(
            split_part(period, '.', 1),
            '-',
            lpad(split_part(period, '.', 2), 2, '0'),
            '-01'
        )
    ) as period_date,

    try_to_decimal(data_value, 18, 8) as data_value,

    trim(status) as status,
    trim(units) as units,
    trim(subject) as subject,
    trim(group_name) as group_name,
    nullif(trim(series_title_1), '') as series_title_1,
    nullif(trim(series_title_2), '') as series_title_2,
    nullif(trim(series_title_3), '') as series_title_3,

    ingested_at,
    source_file

from {{ source('raw', 'STATS_NZ_SELECTED_PRICE_INDEXES') }}