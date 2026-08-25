# Data Sources

## 1. Purpose

This document records the public data source selected for the MVP of the
**NZ Product & Pricing Data Platform**.

The MVP focuses on Stats NZ Selected Price Indexes data, with two
related but distinct business concepts:

1.  **Product Price** --- monthly weighted-average prices for selected
    food products.
2.  **Price Index** --- Food Price Index series used to represent
    broader food price movements.

These concepts are intentionally kept separate because a price index is
not a dollar price.

------------------------------------------------------------------------

## 2. Primary Source

### Provider

**Stats NZ (Tatauranga Aotearoa)**

### Publication

**Selected price indexes: June 2026**

Stats NZ describes Selected Price Indexes (SPI) as monthly price changes
for a selection of goods and services purchased by New Zealand
households.

### Source page

https://www.stats.govt.nz/information-releases/selected-price-indexes-june-2026/

### Data file used for this project

`selected-price-indexes-june-2026.csv`

The downloaded CSV contains the source observations used for the initial
data profiling.

### Format

CSV (Comma Separated Values)

### Publication / update frequency

The Selected Price Indexes publication is monthly. The June 2026 release
was published on 17 July 2026 and provides monthly price information.

### Metadata

Stats NZ DataInfo+ provides metadata for the Selected Price Indexes
series:

https://datainfoplus.stats.govt.nz/item/nz.govt.stats/0775ff1e-457c-4ae3-a28e-ed80c6d19c8f

------------------------------------------------------------------------

## 3. Dataset A --- Product Price

### Dataset

**Food Price Index Selected Monthly Weighted Average Prices for New
Zealand**

### Purpose

This dataset is used for:

-   product-level price analysis
-   historical product price trends
-   product price changes
-   identifying products that may require pricing review

### Source identification

The source CSV contains the following group:

`Food Price Index Selected Monthly Weighted Average Prices for New Zealand`

The group contains **34,708 observations across 155 product series** in
the June 2026 source file.

### Units

`UNITS = Dollars`

This confirms that the selected observations represent monetary product
prices rather than index values.

### Selected MVP fields

  Source field         Purpose in MVP
  -------------------- ------------------------------------
  `Series_reference`   Stable Stats NZ series identifier
  `Period`             Monthly observation period
  `Data_value`         Weighted-average product price
  `STATUS`             Observation status
  `UNITS`              Unit of measurement
  `Subject`            Statistical subject
  `Group`              Source dataset/group
  `Series_title_1`     Product name / product description

`Series_title_2` and `Series_title_3` are retained in the RAW layer
because they are part of the source schema, but they are not currently
required for the product-price MVP model.

### Data grain

The intended analytical grain is:

> **One product series × one month**

`Series_reference` identifies the product series and `Period` identifies
the monthly observation.

The profiling found no duplicate `Series_reference + Period` keys in the
source file.

### Coverage

The product-price group in the June 2026 source file covers:

-   155 product series
-   monthly observations
-   periods from June 2006 through June 2026

Individual series availability should still be treated as
source-controlled and should not be assumed to be identical for future
releases.

------------------------------------------------------------------------

## 4. Dataset B --- Food Price Index

### Purpose

The Food Price Index is used for:

-   category-level price trends
-   broader food price movement
-   comparison with product-level price observations

### Selected MVP series

The MVP will use the following Food Price Index hierarchy:

#### Level 1 --- Food

  Series reference   Series title   Units
  ------------------ -------------- -------
  `CPIM.SE901`       Food           Index

Source group:

`Food Price Index Level 1 Groups for New Zealand Monthly`

This is the overall Food Price Index series.

#### Level 2 --- Food subgroups

The MVP will also include the five Level 2 food subgroups:

  Series reference   Series title                             Units
  ------------------ ---------------------------------------- -------
  `CPIM.SE9011`      Fruit and vegetables                     Index
  `CPIM.SE9012`      Meat, poultry and fish                   Index
  `CPIM.SE9013`      Grocery food                             Index
  `CPIM.SE9014`      Non-alcoholic beverages                  Index
  `CPIM.SE9015`      Restaurant meals and ready-to-eat food   Index

Source group:

`Food Price Index Level 2 Subgroups for New Zealand`

### Why these series were selected

The Level 1 Food series provides the overall benchmark.

The five Level 2 series provide a small, meaningful category hierarchy
that supports comparison between:

-   overall food price movement
-   major food categories
-   individual product prices

Level 3 and Level 4 Food Price Index series are available in the source
but are not required for the MVP. They can be added later if more
detailed category analysis is needed.

### Selected MVP fields

  Source field         Purpose in MVP
  -------------------- -----------------------------
  `Series_reference`   Stats NZ series identifier
  `Period`             Monthly observation period
  `Data_value`         Price index value
  `STATUS`             Observation status
  `UNITS`              Unit of measurement
  `Subject`            Statistical subject
  `Group`              Statistical group
  `Series_title_1`     Food category / series name

### Data grain

The intended analytical grain is:

> **One Food Price Index series × one month**

The selected Level 1 and Level 2 series have unique
`Series_reference + Period` combinations in the profiled source file.

------------------------------------------------------------------------

## 5. Percentage-Change Data

The source also contains:

`Food Price Index for New Zealand, percentage change`

with:

-   `UNITS = Percent`
-   two series:
    -   `CPIM.SE901AC`
    -   `CPIM.SE901PC`

Percentage-change observations are recognised as a separate source
concept.

For the initial MVP, percentage changes will **not** be modelled as a
separate primary fact table. Where appropriate, percentage changes can
be calculated from the monthly observations in dbt or SQL.

The source percentage-change series may be used later for validation or
comparison against calculated results.

------------------------------------------------------------------------

## 6. Source Suitability

The Stats NZ source is suitable for this project because it provides:

-   real New Zealand public data
-   machine-readable CSV data
-   monthly time-series observations
-   product-level weighted-average prices
-   broader Food Price Index series
-   percentage-change information
-   stable series identifiers
-   multiple levels of food classification

This allows the project to demonstrate a realistic data-engineering
workflow without relying on synthetic data for the core pricing
analysis.

------------------------------------------------------------------------

## 7. Known Limitations

### 7.1 Statistical prices are not company transaction prices

The weighted-average product prices are statistical price observations.
They should not be interpreted as the actual purchase price, supplier
price, or sales price of a specific company.

### 7.2 Product catalogue is limited

The product-price dataset contains selected food products rather than a
complete commercial product catalogue.

### 7.3 Category relationships are source-defined

The project should not invent product-to-category relationships that are
not supported by the source data.

The initial MVP therefore treats the Stats NZ product series and Food
Price Index series as separate source concepts.

### 7.4 Historical availability varies by series

Different series can have different historical start dates. The pipeline
should therefore use the actual source period rather than assuming that
every series has the same history.

### 7.5 Period representation requires careful parsing

The source represents monthly periods in a `YYYY.MM` style numeric/text
representation. Values such as `2020.1` represent January 2020, while
`2020.10` represents October 2020.

The ingestion layer must therefore parse the period carefully rather
than treating the raw value as an ordinary decimal number.

### 7.6 Source updates

The project currently uses the June 2026 release. Future monthly
releases may revise historical observations or add new observations.

The ingestion process should therefore be designed so that a new source
file can be processed without changing the core data model
unnecessarily.

------------------------------------------------------------------------

## 8. Why These Two Datasets Form the MVP

The two selected datasets provide complementary analytical levels:

``` text
                 Stats NZ
                    |
          Selected Price Indexes
                    |
          +---------+---------+
          |                   |
          v                   v
    Product Prices       Food Price Index
      Dollars                 Index
          |                   |
          v                   v
 Product-level trends   Category-level trends
          |                   |
          +---------+---------+
                    |
                    v
             Pricing Analysis
```

This gives the project a clear business story while keeping the MVP
small enough to implement end to end.

------------------------------------------------------------------------

## 9. MVP Decision

The MVP will therefore use:

### Dataset A

**Food Price Index Selected Monthly Weighted Average Prices for New
Zealand**

-   155 product series in the June 2026 source file
-   `UNITS = Dollars`
-   monthly observations
-   product-level analysis

### Dataset B

**Food Price Index**

-   Level 1: Food
-   Level 2: five major food subgroups
-   `UNITS = Index`
-   monthly observations
-   category-level analysis

Percentage-change series are retained as a potential
validation/reference dataset but are not required as a separate primary
fact table for the MVP.

------------------------------------------------------------------------

## 10. Source Validation Status

-   [x] Source provider identified
-   [x] Dataset identified
-   [x] Source CSV obtained
-   [x] CSV format confirmed
-   [x] Product-price group confirmed
-   [x] Product prices confirmed as dollars
-   [x] Product-level series confirmed
-   [x] Food Price Index confirmed
-   [x] Food Level 1 series selected
-   [x] Food Level 2 series selected
-   [x] Relevant MVP fields documented
-   [x] Data grain documented
-   [x] Known limitations documented
-   [x] Source suitability documented
