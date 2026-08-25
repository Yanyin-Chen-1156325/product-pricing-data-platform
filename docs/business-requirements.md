# Business Requirements

## 1. Project Purpose

The NZ Product & Pricing Data Platform is a portfolio Data Engineering project that demonstrates how real New Zealand public pricing data can be transformed into trusted, analytics-ready information.

The project simulates a business that needs reliable pricing information to understand product price movements, identify significant changes, and support pricing review.

The first version focuses on Stats NZ pricing data and an end-to-end data pipeline.

---

## 2. Business Problem

Pricing data can contain different structures, time periods, units, classifications, and data-quality issues.

A business needs a reliable data platform that can:

- ingest pricing data from a real public source
- preserve the raw source data
- standardise and transform the data
- validate data quality
- create analytics-ready data models
- support pricing analysis
- provide business-facing reporting

The project therefore focuses on building the data pipeline behind pricing analysis rather than simply analysing a CSV file.

---

## 3. Business Objective

The primary objective is:

> Build a reliable data pipeline that transforms raw New Zealand public pricing data into trusted, analytics-ready data for pricing analysis and reporting.

The project should demonstrate both technical Data Engineering skills and an understanding of how data supports business decisions.

---

## 4. MVP Scope

The MVP will use Stats NZ pricing data as the primary public source.

The initial pipeline is:

```text
Stats NZ
   ↓
Python Ingestion
   ↓
Snowflake RAW
   ↓
dbt
   ↓
Analytics Models
   ↓
Data Quality Tests
   ↓
SQL Analysis
   ↓
Power BI
```

The MVP does not require a second public data source, synthetic business data, Airflow, or other advanced infrastructure.

Those are potential future extensions after the MVP works end to end.

---

## 5. Primary Data Concepts

The MVP uses two distinct pricing concepts.

### 5.1 Product Price

Weighted-average prices for selected food products.

This data is intended to support:

- product-level price analysis
- historical price trends
- product price changes

### 5.2 Price Index

Food Price Index series representing broader price-level movements.

This data is intended to support:

- category-level price trends
- price index analysis
- comparison with product-level prices

### Important Business Rule

A price index value must not be treated as a dollar price.

Product prices and price indexes are therefore modelled as separate business concepts.

---

## 6. Business Questions

The analytics layer should answer the following questions.

### Pricing Trends

1. Which product categories have experienced the largest price increases?
2. How have prices changed over time?
3. Which products have experienced the largest price changes?

### Data Quality

4. Which records have missing, invalid, duplicate, or inconsistent data?

### Pricing Review

5. Which products or categories may require pricing review based on significant price changes?

---

## 7. Functional Requirements

### FR-01 — Data Ingestion

The system shall ingest the selected Stats NZ pricing data using Python.

### FR-02 — Data Validation

The ingestion process shall validate required columns, data types, dates, missing values, and duplicate records where applicable.

### FR-03 — Raw Data Storage

The system shall store source data in a Snowflake RAW layer with minimal transformation.

### FR-04 — Data Transformation

dbt shall transform the RAW data into clean staging and analytics-ready models.

### FR-05 — Data Quality

The platform shall implement automated data-quality tests for important fields and relationships.

### FR-06 — Analytics Model

The platform shall provide analytics-ready models for product prices and price indexes.

### FR-07 — Business Analysis

SQL queries shall answer the defined business questions using the analytics models.

### FR-08 — Reporting

Power BI shall provide business-facing views of pricing trends, product price changes, and data quality.

---

## 8. Non-Functional Requirements

### NFR-01 — Reproducibility

Another developer should be able to understand how the pipeline works from the GitHub repository.

### NFR-02 — Maintainability

The repository should separate ingestion, transformation, analytics, documentation, and reporting.

### NFR-03 — Data Quality

Important assumptions and data-quality rules should be explicitly documented and tested.

### NFR-04 — Security

Credentials, passwords, API keys, and other secrets must not be committed to GitHub.

### NFR-05 — Traceability

The final analytics data should be traceable back to the source data through the pipeline layers.

### NFR-06 — Portfolio Evidence

Each major technical capability should have visible evidence in the repository.

---

## 9. Data Quality Requirements

The project will use appropriate checks including:

- required fields are not NULL
- expected unique keys are unique
- categorical values use expected values
- dates are valid
- numeric values are valid
- duplicate records are identified
- relationships are valid where applicable

The exact tests will be finalised after detailed source profiling.

---

## 10. Data Model Requirements

The initial analytics model is expected to contain:

```text
dim_date
dim_product

fact_product_price
fact_price_index
```

The final structure and grain will be confirmed after source profiling.

The model must keep product prices and price indexes conceptually separate.

---

## 11. Reporting Requirements

The Power BI MVP should provide:

### Executive Overview

- overall pricing trend
- product/category comparisons
- significant price changes
- basic data-quality indicators

### Product Pricing

- selected product price
- historical price trend
- price changes
- top increases/decreases

### Data Quality

- record counts
- missing data
- duplicate records
- invalid records
- test results or quality indicators

---

## 12. Success Criteria

The MVP is successful when:

- [ ] Stats NZ pricing data can be ingested successfully
- [ ] Raw data is stored in Snowflake
- [ ] dbt staging models run successfully
- [ ] Analytics models are implemented
- [ ] Data-quality tests pass
- [ ] SQL queries answer the defined business questions
- [ ] Power BI displays the analytics results
- [ ] The complete pipeline is documented in GitHub

The project should demonstrate a complete path from source data to business-ready information.

---

## 13. Future Scope

After the MVP is complete, potential extensions include:

### Second Public Data Source

Stats NZ Input-Output Tables may be added to demonstrate multi-source integration and more complex data modelling.

### Synthetic Business Data

Synthetic products, suppliers, customers, sales, or internal price-list data may be added to simulate internal business systems.

### Automation

The manual pipeline may later be automated with a scheduler or GitHub Actions.

Advanced orchestration such as Airflow should only be added if it provides a meaningful architectural benefit.

---

## 14. Out of Scope for MVP

The following are intentionally outside the initial MVP:

- [ ] Second public data source
- [ ] Synthetic business systems
- [ ] Airflow
- [ ] Kubernetes
- [ ] Kafka
- [ ] Databricks
- [ ] PySpark
- [ ] Microservices
- [ ] Real-time streaming

The goal is to complete a reliable end-to-end batch data pipeline before adding complexity.
