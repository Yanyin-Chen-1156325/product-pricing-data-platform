# Data Quality

## 1. Purpose

This document describes the data quality checks implemented for the
product pricing data platform.

The goal is to ensure that the analytics models are structurally valid,
referentially consistent, and suitable for downstream analysis.

Data quality checks are implemented using dbt tests.

---

## 2. Data Quality Strategy

The data quality layer validates the analytics models across the following areas:

- Required fields are not null
- Primary and business keys are unique
- Accepted values are valid
- Foreign key relationships are valid
- Fact table grain is respected
- Numeric measures are populated

The tests are applied to:

- `dim_date`
- `dim_product`
- `fact_product_price`
- `fact_price_index`

---

## 3. Tests Implemented

### 3.1 Not-null Tests

Not-null tests are applied to required analytical fields, including:

- `dim_date.date_key`
- `dim_date.date`
- `dim_date.year`
- `dim_date.month`
- `dim_product.product_key`
- `dim_product.series_reference`
- `dim_product.product_name`
- `fact_product_price.date_key`
- `fact_product_price.product_key`
- `fact_product_price.price`
- `fact_price_index.date_key`
- `fact_price_index.series_reference`
- `fact_price_index.index_value`

---

### 3.2 Uniqueness Tests

Uniqueness tests are applied to dimension keys and identifiers:

- `dim_date.date_key`
- `dim_date.date`
- `dim_product.product_key`
- `dim_product.series_reference`

These tests help ensure that dimension records follow their expected grain.

---

### 3.3 Accepted Values Tests

Controlled fields are validated using accepted-value tests.

#### Product Price

`fact_product_price.units` must contain:

```text
Dollars
```

`fact_product_price.status` must contain one of:

```text
FINAL
REVISED
```

#### Price Index

`fact_price_index.units` must contain:

```text
Index
```

`fact_price_index.status` must contain one of:

```text
FINAL
REVISED
```

---

### 3.4 Relationship Tests

Foreign key relationships are validated using dbt relationship tests.

```text
fact_product_price.date_key
    → dim_date.date_key

fact_product_price.product_key
    → dim_product.product_key

fact_price_index.date_key
    → dim_date.date_key
```

These tests ensure that fact records reference valid dimension records.

---

### 3.5 Fact Table Grain Tests

The fact tables represent monthly observations, so their business grain is
explicitly tested.

#### `fact_product_price`

Grain:

```text
One product × one month
```

The combination of:

```text
product_key + date_key
```

must be unique.

#### `fact_price_index`

Grain:

```text
One price index series × one month
```

The combination of:

```text
series_reference + date_key
```

must be unique.

These checks are implemented as dbt singular tests.

---

## 4. Test Results

The dbt test suite contains 26 data tests.

Latest test result:

```text
PASS = 26
WARN = 0
ERROR = 0
SKIP = 0
TOTAL = 26
```

All configured data quality tests passed successfully.

The tests cover:

- Not-null validation
- Uniqueness validation
- Accepted-value validation
- Referential integrity
- Fact table grain

---

## 5. Source Data Quality Findings

Source validation identified records with missing `data_value` values.

### Product Price

```text
Dollars records:       34,708
Valid price records:   34,626
Records excluded:          82
```

The 82 records with null `data_value` are excluded from
`fact_product_price`.

### Price Index

```text
Index records:         23,228
Valid index records:   23,219
Records excluded:           9
```

The 9 records with null `data_value` are excluded from
`fact_price_index`.

These records are excluded because a missing measure cannot form a valid
analytical observation.

The raw source data is preserved separately so the original records remain
traceable.

---

## 6. Data Modelling Quality Rules

Product Price and Price Index are treated as separate business concepts.

A product price represents a monetary value, while a price index represents
an index value.

Therefore:

```text
Product Price
→ Dollars

Price Index
→ Index
```

Index values are not treated as dollar prices.

The model also avoids inventing unsupported product hierarchies.
Product information is derived from the Stats NZ source fields rather than
creating categories that are not supported by the source data.

---

## 7. Data Quality Limitations

The source data contains some records with missing `data_value` values.

These records are retained in the raw layer but excluded from the analytics
fact tables.

The current model does not estimate, interpolate, or replace missing source
values.

This preserves the original source meaning and avoids introducing
unsupported assumptions into the analytical dataset.

---

## 8. Validation Commands

Run all dbt data quality tests with:

```bash
dbt test
```

Run the complete dbt transformation pipeline with:

```bash
dbt run
```

---

## 9. Current Status

The analytics data model has passed all configured dbt data quality tests.

```text
dim_date              Validated
dim_product           Validated
fact_product_price    Validated
fact_price_index      Validated
```

The current data quality test suite provides automated validation for the
core analytics models and their business grain.
