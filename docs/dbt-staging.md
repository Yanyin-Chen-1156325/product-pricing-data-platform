# dbt Staging Transformations

## 1. Purpose

The staging layer transforms the Stats NZ source data stored in
Snowflake RAW into a clean and consistent representation for downstream
analytics models.

The transformation boundary is:

``` text
Stats NZ CSV
    |
    v
Python ingestion
    |
    v
Snowflake RAW
    |
    v
dbt staging
    |
    v
Snowflake STAGING
```

Business-specific calculations are not performed in the staging layer.

## 2. Source

Source table:

``` text
PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES
```

dbt source configuration:

``` text
source('raw', 'STATS_NZ_SELECTED_PRICE_INDEXES')
```

Staging model:

``` text
STG_STATS_NZ_SELECTED_PRICE_INDEXES
```

Materialization:

``` text
Snowflake VIEW
```

## 3. Source-to-Staging Transformations

  -----------------------------------------------------------------------------
  Source field         Staging field        Transformation    Reason
  -------------------- -------------------- ----------------- -----------------
  `SERIES_REFERENCE`   `series_reference`   Standardised to   Consistent naming
                                            snake_case and    and clean
                                            trimmed           identifiers

  `PERIOD`             `period_date`        Convert `YYYY.MM` Supports reliable
                                            to a `DATE` using date filtering
                                            the first day of  and time-series
                                            the month         analysis

  `DATA_VALUE`         `data_value`         Convert to        Provides a
                                            decimal           numeric measure
                                                              for analysis

  `STATUS`             `status`             Trim whitespace   Preserve source
                                                              status while
                                                              standardising
                                                              text

  `UNITS`              `units`              Trim whitespace   Preserve the
                                                              source unit
                                                              semantics

  `SUBJECT`            `subject`            Trim whitespace   Standardise
                                                              source text

  `GROUP_NAME`         `group_name`         Trim whitespace   Standardise
                                                              source text

  `SERIES_TITLE_1`     `series_title_1`     Trim whitespace;  Standardise text
                                            empty strings     and missing-value
                                            become NULL       representation

  `SERIES_TITLE_2`     `series_title_2`     Trim whitespace;  Preserve optional
                                            empty strings     source metadata
                                            become NULL       

  `SERIES_TITLE_3`     `series_title_3`     Trim whitespace;  Preserve optional
                                            empty strings     source metadata
                                            become NULL       

  `INGESTED_AT`        `ingested_at`        Retained          Preserve
                                                              ingestion
                                                              metadata for
                                                              traceability

  `SOURCE_FILE`        `source_file`        Retained          Preserve
                                                              source-file
                                                              lineage
  -----------------------------------------------------------------------------

## 4. Period Transformation

The source represents monthly observations using `YYYY.MM`.

Examples:

``` text
1960.01 -> 1960-01-01
1960.02 -> 1960-02-01
2024.10 -> 2024-10-01
```

The first day of the month is used as the analytical date because the
source observation represents a monthly period rather than a specific
transaction date.

## 5. Missing Values

The source contains missing `DATA_VALUE` observations.

Missing values are not converted to zero.

For optional text fields, empty strings are converted to SQL `NULL`
where appropriate.

`SERIES_TITLE_2` and `SERIES_TITLE_3` may legitimately contain many NULL
values because those title levels are not populated for every source
series.

## 6. Status Handling

The source contains both `FINAL` and `REVISED` observations.

The staging model preserves these source statuses rather than filtering
them out.

This allows downstream models and analysis to decide how observation
status should be used.

## 7. Units Handling

The source contains multiple unit concepts, including:

-   `Dollars`
-   `Index`
-   `Percent`

The staging model preserves `units` as a separate field.

The transformation does not combine these values into a generic price
measure because an index or percentage value is not the same business
concept as a dollar price.

## 8. Staging Model SQL

The current model is:

``` sql
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
```

## 9. Design Boundary

The staging layer focuses on source-oriented cleaning and
standardisation.

It does not:

-   calculate price changes
-   calculate year-over-year changes
-   create business KPIs
-   combine product prices and price indexes
-   invent unsupported product hierarchies

Those transformations belong in later analytics or mart models.

## 10. Result

The staging model provides a clean source-oriented layer:

``` text
PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES
                    |
                    | dbt source()
                    v
PRODUCT_PRICING_DB.STAGING.STG_STATS_NZ_SELECTED_PRICE_INDEXES
```

This creates a clear separation between ingestion data and transformed
analytics data.
