# NZ Product & Pricing Data Platform

A portfolio Data Engineering project that transforms real New Zealand public pricing data into trusted, analytics-ready data for business reporting.

## Project Overview

This project simulates a company that manages product and pricing information and needs a reliable data platform for pricing analysis and business reporting.

The platform will ingest public New Zealand data, store the raw data in Snowflake, transform and test it with dbt, and expose business-ready data for SQL analysis and Power BI.

The project is designed to demonstrate practical skills in:

- Python data ingestion
- ETL / ELT
- SQL
- Snowflake
- dbt
- Data modelling
- Data quality
- Business analytics
- Power BI
- Git / GitHub
- Cloud-ready data architecture

## Business Problem

Pricing data is often collected from multiple sources and may contain different structures, time periods, units, classifications, and data-quality issues.

A business needs a reliable way to:

- understand how product prices change over time
- identify products or categories with significant price increases
- maintain consistent, analytics-ready data
- detect missing, invalid, or inconsistent records
- provide trusted information for pricing review and decision-making

This project demonstrates how a modern data pipeline can turn raw public data into business-ready information.

## Project Objectives

### 1. Demonstrate Data Engineering

Build a complete pipeline from source data to analytics.

### 2. Demonstrate Business Data Management

Work with concepts such as:

- products
- pricing
- classifications
- data quality
- business reporting

### 3. Demonstrate Modern Data Platform Skills

Use Python, Snowflake, dbt, SQL, and Power BI without adding unnecessary technologies.

### 4. Connect Existing Experience to Data Engineering

The project builds on experience with:

- SQL
- ETL / SSIS
- relational databases
- data integration
- business applications
- production systems

The intended career progression is:

```text
Software Engineering
        +
SQL / ETL / Integration
        |
        v
Data Engineering
```

## Architecture

The target MVP architecture is:

```text
                Public Data Sources
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
             +---------+---------+
             |                   |
             v                   v
          Staging             Marts
                                 |
                       +---------+---------+
                       |                   |
                       v                   v
                  SQL Analysis        Power BI
```

The core principle is to keep raw source data separate from transformed analytics data.

## Data Sources

The primary source for the MVP is Stats NZ price data.

### Stats NZ Selected Price Indexes

The dataset provides New Zealand price-related time series, including:

- Food Price Index data
- weighted-average product prices
- price index values
- monthly observations
- product and category-related metadata

Two main data concepts will be used:

### Product Price

Weighted-average prices for selected food products.

Used for:

- product-level price analysis
- historical price trends
- product price changes

### Price Index

Price index series representing broader price-level movements.

Used for:

- category-level price trends
- price index analysis
- comparison with product-level prices

Product prices and price indexes are treated as separate business concepts because an index value is not a dollar price.

More detailed source documentation will be added in:

```text
docs/data-sources.md
```

## Business Questions

The analytics layer will answer a small set of business questions.

### Pricing

1. Which product categories have experienced the largest price increases?
2. How have prices changed over time?
3. Which products have experienced the largest price changes?

### Data Quality

4. Which records have missing, invalid, or inconsistent data?

### Business Decision Support

5. Which products or categories should be reviewed for pricing changes?

## Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Data Warehouse | Snowflake |
| Transformation | dbt |
| Query | SQL |
| BI | Power BI |
| Version Control | Git / GitHub |
| Testing | pytest, dbt tests |

Optional technologies may be added only when there is a clear technical reason.

The MVP intentionally does not require:

- Databricks
- PySpark
- Kafka
- Airflow
- Kubernetes
- Microservices

## Data Layers

### RAW

Raw source data is stored as close to the source structure as practical.

Example:

```text
RAW
└── STATS_NZ_PRICE_INDEXES
```

The RAW layer should not contain business transformations.

### STAGING

dbt is used to:

- standardise column names
- convert data types
- standardise dates
- handle appropriate NULL values
- prepare source data for modelling

### INTERMEDIATE

Reusable transformation logic can be placed here when needed.

### MARTS

Business-ready analytics models will be created here.

Initial model:

```text
dim_date
dim_product

fact_product_price
fact_price_index
```

The exact model will be finalised after source profiling.

## Data Quality

Data quality is a core part of the project rather than an afterthought.

Planned checks include:

- NOT NULL
- UNIQUE
- accepted values
- valid dates
- valid numeric values
- duplicate detection
- relationship validation
- missing-data checks

The project will document the rules and show representative test results.

## MVP Scope

The first milestone is intentionally small.

```text
Stats NZ
   ↓
Python
   ↓
Snowflake RAW
   ↓
dbt
   ↓
Analytics Models
   ↓
Data Quality Tests
   ↓
SQL
   ↓
Power BI
```

The MVP is complete when the full pipeline works end to end.

## Future Extensions

After the MVP works, the project may be extended with:

### Second Public Data Source

Stats NZ Input-Output Tables can be added to demonstrate multi-source integration and more complex data modelling.

### Synthetic Business Data

Clearly labelled synthetic data may simulate internal business systems such as:

- suppliers
- products
- customers
- sales
- internal price lists

Synthetic data will only be used where public data cannot represent the required business context.

### Automation

After the manual pipeline is stable, the pipeline may be automated with a scheduler or GitHub Actions.

Airflow will only be considered if it provides a meaningful architectural benefit.



