# Data Model

## 1. Overview

The data model transforms cleaned Stats NZ price data into analytics-ready tables for SQL analysis and Power BI.

The model separates descriptive attributes from measurable observations using a simple dimensional modelling approach.

### Core model

```text
dim_date
    |
    +-------------------------+
    |                         |
    v                         v
fact_product_price     fact_price_index
    |
    v
dim_product
```

The model contains four core tables:

- `dim_date`
- `dim_product`
- `fact_product_price`
- `fact_price_index`

---

## 2. Data Sources and Scope

The initial model is based on the Stats NZ Selected Price Indexes data.

The source contains different types of observations identified by the `UNITS` field:

- `Dollars` — weighted-average product prices
- `Index` — price index observations
- `Percent` — percentage change observations

For the MVP, the model focuses on:

- Product price observations (`Dollars`)
- Price index observations (`Index`)

Percentage change observations (`Percent`) are not modelled as a separate fact table in the current MVP.

This keeps the model focused on the core business concepts while avoiding unnecessary tables.

---

## 3. Dimensional Modelling Approach

The model uses two types of tables:

### Dimension tables

Dimension tables provide descriptive information used to analyse facts.

```text
dim_date
dim_product
```

### Fact tables

Fact tables contain measurable business observations at a defined grain.

```text
fact_product_price
fact_price_index
```

The grain of each fact table is explicitly defined to prevent duplicate or ambiguous observations.

---

# 4. `dim_date`

## Purpose

Provide reusable calendar attributes for time-based analysis.

The source data is monthly, so the date dimension uses a monthly grain.

## Grain

```text
One row per month
```

## Suggested structure

| Column | Description |
|---|---|
| `date_key` | Surrogate date key |
| `date` | Representative date for the month |
| `year` | Calendar year |
| `month` | Calendar month number |
| `month_name` | Calendar month name |
| `year_month` | Year-month representation |

## Key

```text
Primary Key:
date_key
```

## Design decision

The source data uses monthly periods. Therefore, a monthly date dimension is sufficient for the current project scope.

Additional calendar attributes should only be added when they provide value for the planned analysis or Power BI reporting.

---

# 5. `dim_product`

## Purpose

Store descriptive information for products in the selected Stats NZ weighted-average-price dataset.

The product dimension represents the product price series rather than individual physical products or transactions.

## Grain

```text
One row per product price series
```

## Suggested structure

| Column | Description |
|---|---|
| `product_key` | Surrogate product key |
| `series_reference` | Stats NZ series identifier |
| `product_name` | Product description from the source |

## Key

```text
Primary Key:
product_key
```

The Stats NZ `series_reference` is retained as the source business identifier.

## Product identification

For the selected weighted-average-price dataset, the product name is derived from the source series information.

The model should retain the original Stats NZ `series_reference` so that each product can be traced back to the source data.

## Product hierarchy

No additional product/category hierarchy is created unless a reliable relationship is explicitly supported by the source data.

The project should not invent product-to-category relationships that cannot be validated from the source.

---

# 6. `fact_product_price`

## Purpose

Store monthly weighted-average product price observations.

This table represents the actual dollar price observations provided by the Stats NZ selected monthly weighted-average-price dataset.

## Grain

```text
One product × one month
```

Each row represents the price observation for one product for one month.

## Suggested structure

| Column | Description |
|---|---|
| `date_key` | Foreign key to `dim_date` |
| `product_key` | Foreign key to `dim_product` |
| `price` | Observed product price |
| `status` | Source observation status |
| `units` | Source unit, expected to represent dollars |

## Keys

```text
Foreign Keys:
date_key → dim_date.date_key
product_key → dim_product.product_key
```

The logical grain is:

```text
product_key + date_key
```

This combination should uniquely identify a product price observation.

## Source mapping

| Source field | Model field |
|---|---|
| `Series_reference` | `dim_product.series_reference` |
| `Period` | `dim_date.date` / `date_key` |
| `Data_value` | `price` |
| `STATUS` | `status` |
| `UNITS` | `units` |

Only observations representing dollar-based weighted-average product prices should be loaded into this fact table.

---

# 7. `fact_price_index`

## Purpose

Store monthly price index observations from Stats NZ.

Price index values represent an index measure and must not be interpreted as dollar prices.

## Grain

```text
One price index series × one month
```

Each row represents one price index series observation for one month.

## Suggested structure

| Column | Description |
|---|---|
| `date_key` | Foreign key to `dim_date` |
| `series_reference` | Stats NZ price index series identifier |
| `index_value` | Price index observation |
| `status` | Source observation status |
| `units` | Source unit, expected to represent an index |

## Keys

```text
Foreign Key:
date_key → dim_date.date_key
```

The logical grain is:

```text
series_reference + date_key
```

This combination should uniquely identify a price index observation.

## Source mapping

| Source field | Model field |
|---|---|
| `Series_reference` | `series_reference` |
| `Period` | `dim_date.date` / `date_key` |
| `Data_value` | `index_value` |
| `STATUS` | `status` |
| `UNITS` | `units` |

Only observations representing price index values should be loaded into this fact table.

---

# 8. Product Price vs Price Index

Product prices and price indexes are separate business concepts and are therefore stored in separate fact tables.

### Product price

```text
Example:

Product: Apples
Price: $5.80
```

This represents an observed dollar price for a product.

### Price index

```text
Example:

Food Price Index: 125.4
```

This represents an index value rather than a dollar price.

The two measures should not be combined into a single price measure.

---

# 9. Percentage Change Data

The source also contains observations with:

```text
UNITS = Percent
```

These represent percentage change measures.

They are not included as a separate fact table in the current MVP.

This is an intentional scope decision.

Percentage changes can be considered later if they are required for business analysis or Power BI reporting.

---

# 10. Relationships

The core relationships are:

```text
dim_date
    |
    +----------------------+
    |                      |
    v                      v
fact_product_price    fact_price_index
    |
    v
dim_product
```

### Relationships

```text
dim_date.date_key
        ↓
fact_product_price.date_key
```

```text
dim_product.product_key
        ↓
fact_product_price.product_key
```

```text
dim_date.date_key
        ↓
fact_price_index.date_key
```

The current model does not establish a direct relationship between `dim_product` and `fact_price_index`.

This is because the product price series and price index series represent different statistical concepts and the source does not provide a validated product-to-index relationship for the current scope.

---

# 11. Key Design Decisions

## 11.1 Use surrogate keys for dimensions

`dim_date` and `dim_product` use internal keys:

```text
date_key
product_key
```

These provide stable keys for relationships within the analytics model.

The original Stats NZ `series_reference` is retained as the source identifier.

---

## 11.2 Preserve source identifiers

The original `series_reference` is retained rather than replaced entirely by an internal key.

This supports:

- source traceability
- data validation
- troubleshooting
- reconciliation with Stats NZ data

---

## 11.3 Define fact grain explicitly

The fact table grain is defined before implementation.

```text
fact_product_price
→ one product × one month

fact_price_index
→ one price index series × one month
```

This allows duplicate observations to be detected and tested.

---

## 11.4 Do not invent unsupported hierarchy

The source data contains different statistical groupings and index levels.

However, the model does not assume that these automatically represent a product category hierarchy.

Product/category relationships should only be introduced when they can be reliably supported by the source data.

---

## 11.5 Keep business concepts separate

Product prices and price indexes have different meanings, units, and analytical purposes.

They are therefore stored separately:

```text
fact_product_price
        +
fact_price_index
```

rather than being combined into a single fact table.

---

# 12. Data Quality Expectations

The following checks should be applied when the model is implemented:

### `dim_date`

- `date_key` should be unique
- `date` should not be null
- Each month should have one row

### `dim_product`

- `product_key` should be unique
- `series_reference` should not be null
- Product names should be populated where provided by the source

### `fact_product_price`

- `date_key` should not be null
- `product_key` should not be null
- `price` should be numeric
- `product_key + date_key` should be unique
- `units` should represent dollar observations

### `fact_price_index`

- `date_key` should not be null
- `series_reference` should not be null
- `index_value` should be numeric
- `series_reference + date_key` should be unique
- `units` should represent index observations

---

# 13. Implementation

The model will be implemented using dbt.

Target structure:

```text
dbt/
└── models/
    ├── staging/
    │   └── stg_stats_nz_price_indexes.sql
    │
    └── marts/
        ├── dim_date.sql
        ├── dim_product.sql
        ├── fact_product_price.sql
        └── fact_price_index.sql
```

The staging model will standardise the raw Stats NZ data before the data is transformed into the analytics-ready model.

---

# 14. Validation

Before considering the data model complete, validate:

- [ ] Fact table grains are correct
- [ ] No duplicate product × month observations
- [ ] No duplicate index series × month observations
- [ ] Dimension keys are unique
- [ ] Foreign key relationships are valid
- [ ] Product prices contain only dollar observations
- [ ] Price indexes contain only index observations
- [ ] No unsupported product/category relationships have been introduced

---

# 15. Future Extensions

The model may be extended if future project requirements justify it.

Potential additions include:

```text
dim_category
dim_supplier
fact_sales
fact_customer_activity
```

These are intentionally outside the current MVP because the required source data and business requirements have not yet been established.

Future extensions should only be added when they provide clear business or portfolio value.

---

## Summary

The current analytics model is intentionally simple:

```text
                    dim_date
                       |
             +---------+---------+
             |                   |
             v                   v
   fact_product_price     fact_price_index
             |
             v
       dim_product
```

The model provides a clear separation between:

- descriptive dimensions
- product price observations
- price index observations
- calendar attributes

The design prioritises clear business grain, source traceability, data quality, and analytical usability while avoiding unsupported assumptions about the source data.