-- Post-load validation queries for the Stats NZ RAW table.
-- These queries are read-only and do not modify data.

-- 1. Confirm the expected source record count (59,519 for June 2026).
SELECT COUNT(*) AS row_count
FROM PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES;

-- 2. Confirm the source unit distribution.
SELECT
    UNITS,
    COUNT(*) AS row_count
FROM PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES
GROUP BY UNITS
ORDER BY UNITS;

-- Expected: Dollars = 34,708; Index = 23,228; Percent = 1,583.

-- 3. Confirm the source status distribution.
SELECT
    STATUS,
    COUNT(*) AS row_count
FROM PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES
GROUP BY STATUS
ORDER BY STATUS;

-- Expected: FINAL = 54,635; REVISED = 4,884.

-- 4. Confirm the expected number of missing measurements (91).
SELECT COUNT(*) AS missing_data_value_count
FROM PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES
WHERE DATA_VALUE IS NULL;

-- 5. Check that the source natural key remains unique.
SELECT
    SERIES_REFERENCE,
    PERIOD,
    COUNT(*) AS record_count
FROM PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES
GROUP BY
    SERIES_REFERENCE,
    PERIOD
HAVING COUNT(*) > 1
ORDER BY
    SERIES_REFERENCE,
    PERIOD;

-- Expected: no rows returned.

-- 6. Confirm the load metadata assigned by Snowflake.
SELECT
    SOURCE_FILE,
    COUNT(*) AS row_count,
    MIN(INGESTED_AT) AS first_ingested_at,
    MAX(INGESTED_AT) AS last_ingested_at
FROM PRODUCT_PRICING_DB.RAW.STATS_NZ_SELECTED_PRICE_INDEXES
GROUP BY SOURCE_FILE
ORDER BY SOURCE_FILE;
