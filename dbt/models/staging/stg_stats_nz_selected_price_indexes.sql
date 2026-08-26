select
    series_reference,
    period,
    data_value,
    status,
    units,
    subject,
    group_name,
    series_title_1,
    series_title_2,
    series_title_3,
    ingested_at,
    source_file
from {{ source('raw', 'STATS_NZ_SELECTED_PRICE_INDEXES') }}