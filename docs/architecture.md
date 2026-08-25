# Architecture

## 1. Architecture Overview

The MVP uses a layered data architecture:

```text
                 Stats NZ
             Public Pricing Data
                      |
                      v
              Python Ingestion
                      |
                      v
              Snowflake RAW
                      |
                      v
                     dbt
                      |
          +-----------+-----------+
          |                       |
          v                       v
       Staging                  Marts
                                  |
                       +----------+----------+
                       |                     |
                       v                     v
                  SQL Analysis          Power BI
```

The architecture separates raw source data, transformation logic, analytics models, and business reporting.

---

## 2. Architecture Principles

### Principle 1 — Preserve Raw Data

The RAW layer should remain close to the source structure.

Business transformations should not be performed in RAW.

### Principle 2 — Transform with dbt

Transformations should be implemented in dbt rather than hidden inside ingestion code.

### Principle 3 — Test the Data

Data quality checks should be implemented as part of the transformation pipeline.

### Principle 4 — Separate Business Concepts

Product prices and price indexes represent different concepts and should not be treated as interchangeable.

### Principle 5 — Build MVP First

The first version should use a simple, understandable batch architecture.

Additional technologies should only be introduced when they solve a demonstrated problem.

---

## 3. Source Layer

### Primary Source

Stats NZ pricing data is the primary source for the MVP.

The source contains pricing time-series information, including product price and price index concepts.

The source is external to the platform.

```text
Stats NZ
   |
   | Public pricing data
   v
Python Ingestion
```

The source documentation is maintained separately in:

```text
docs/data-sources.md
```

---

## 4. Ingestion Layer

Python is responsible for obtaining and validating the source data before loading it into the warehouse.

### Responsibilities

- retrieve/read source data
- validate required columns
- validate data types
- parse dates
- identify missing values
- identify duplicate records
- perform source-level validation
- load data into Snowflake

### Boundary

Python ingestion should focus on source acquisition and ingestion-related validation.

Business transformations belong in dbt.

```text
Stats NZ
   |
   v
Python
   |
   +--> Source validation
   |
   v
Snowflake RAW
```

---

## 5. Snowflake RAW Layer

Snowflake is the cloud data warehouse for the project.

The RAW layer stores source data with minimal transformation.

Example:

```text
SNOWFLAKE
└── RAW
    └── STATS_NZ_PRICE_INDEXES
```

### RAW Responsibilities

- preserve source records
- provide a stable source layer for downstream transformations
- support traceability
- separate ingestion from analytics transformations

The RAW layer should not contain business-specific calculations.

---

## 6. dbt Transformation Layer

dbt is responsible for transforming Snowflake RAW data into analytics-ready models.

The transformation flow is:

```text
RAW
 |
 v
STAGING
 |
 v
INTERMEDIATE
 |
 v
MARTS
```

The intermediate layer will only be used where reusable transformation logic is needed.

---

## 7. Staging Layer

The staging layer performs source-oriented transformations.

Typical responsibilities:

- standardise column names
- convert data types
- convert `Period` into a date representation
- standardise NULL values
- standardise source fields
- expose a clean version of the source data

Example:

```text
raw_stats_nz_price_indexes
              |
              v
stg_stats_nz_price_indexes
```

---

## 8. Analytics / Mart Layer

The initial analytics model is:

```text
dim_date
dim_product

fact_product_price
fact_price_index
```

### `dim_date`

Provides calendar attributes for analysis.

Potential attributes include:

- date key
- date
- year
- month

### `dim_product`

Represents the selected product-level pricing series.

Potential attributes include:

- product key
- Stats NZ series reference
- product name

The exact product attributes will be determined from source profiling.

### `fact_product_price`

Represents product-level weighted-average prices.

Expected grain:

```text
one product × one month
```

### `fact_price_index`

Represents price-index observations.

Expected grain:

```text
one price series × one month
```

The exact grain will be validated against the source before implementation.

---

## 9. Data Quality Layer

Data quality is implemented within the dbt transformation workflow.

Conceptually:

```text
RAW
 |
 v
dbt Models
 |
 +--> Data Quality Tests
 |
 v
Analytics Models
```

Planned checks include:

- not-null
- unique
- accepted values
- valid dates
- valid numeric values
- duplicate detection
- relationship validation

The tests should validate assumptions made by the data model.

---

## 10. Analytics Layer

SQL is used to answer business questions against the analytics models.

Example flow:

```text
fact_product_price
        |
        +--> price trends
        |
        +--> product changes
        |
        +--> category analysis

fact_price_index
        |
        +--> index trends
        |
        +--> broader price movement
```

The SQL layer should use business-ready models rather than repeatedly querying raw source tables.

---

## 11. Reporting Layer

Power BI consumes analytics-ready data.

```text
dbt Marts
    |
    v
Power BI
    |
    +--> Executive Overview
    +--> Product Pricing
    +--> Data Quality
```

The dashboard should focus on the business questions defined in `docs/business-requirements.md`.

---

## 12. End-to-End Data Flow

The complete MVP flow is:

```text
1. Stats NZ
      |
      v
2. Python Ingestion
      |
      | source validation
      v
3. Snowflake RAW
      |
      v
4. dbt Staging
      |
      v
5. dbt Intermediate
      |
      v
6. dbt Marts
      |
      +------------------+
      |                  |
      v                  v
7. SQL Analysis      8. Power BI
```

---

## 13. Data Lineage

The expected lineage is:

```text
Stats NZ
   |
   v
raw_stats_nz_price_indexes
   |
   v
stg_stats_nz_price_indexes
   |
   +-----------------------------+
   |                             |
   v                             v
fact_product_price         fact_price_index
   |                             |
   +-------------+---------------+
                 |
                 v
            SQL / Power BI
```

The exact dbt lineage will be updated after the models are implemented.

---

## 14. Repository-to-Architecture Mapping

The GitHub repository mirrors the architecture.

```text
docs/
    |
    +--> architecture.md
    +--> data-sources.md
    +--> data-model.md
    +--> data-quality.md

ingestion/
    |
    +--> Python ingestion
    +--> Python tests

dbt/
    |
    +--> staging
    +--> intermediate
    +--> marts
    +--> dbt tests

sql/
    |
    +--> business analysis queries

powerbi/
    |
    +--> dashboard documentation
    +--> screenshots
```

This makes the repository itself evidence of the data pipeline.

---

## 15. Security

Credentials must not be stored in the repository.

Do not commit:

- Snowflake passwords
- API keys
- access tokens
- private connection strings
- local secret files

Secrets should be supplied through environment variables or an appropriate local/CI secret mechanism.

---

## 16. MVP Technology Decisions

| Layer | Technology | Purpose |
|---|---|---|
| Source | Stats NZ | Public pricing data |
| Ingestion | Python | Data acquisition and source validation |
| Warehouse | Snowflake | Cloud data warehouse |
| Transformation | dbt | SQL-based transformation |
| Testing | pytest + dbt tests | Code and data quality |
| Analytics | SQL | Business analysis |
| BI | Power BI | Reporting |
| Version Control | GitHub | Code and project evidence |

---

## 17. Future Architecture Extensions

These are not part of the initial MVP.

### Multi-source integration

```text
Stats NZ Prices
       +
Stats NZ Input-Output Tables
       |
       v
   Snowflake
```

### Synthetic internal business data

```text
Public Data
     +
Synthetic Business Data
     |
     v
Unified Analytics Model
```

### Automation

```text
Scheduler / GitHub Actions
          |
          v
Python Ingestion
          |
          v
Snowflake
          |
          v
dbt Run
          |
          v
dbt Test
```

Automation should only be introduced after the manual pipeline is stable.

---

## 18. Architecture Success Criteria

- [ ] Data flows from Stats NZ into Python
- [ ] Python loads validated data into Snowflake RAW
- [ ] dbt transforms RAW into analytics models
- [ ] dbt tests validate important assumptions
- [ ] SQL queries use analytics-ready data
- [ ] Power BI consumes the analytics layer
- [ ] Data lineage is documented
- [ ] Repository structure reflects the architecture
- [ ] No credentials or secrets are committed
