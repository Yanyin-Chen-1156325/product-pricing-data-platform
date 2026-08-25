# Data Profile

## 1. Profile Scope

This document records the initial profiling of:

`selected-price-indexes-june-2026.csv`

The file is the Stats NZ Selected Price Indexes CSV used for the MVP
source-validation phase.

The profiling was performed before designing the Snowflake and dbt
models so that the data model is based on the actual source structure.

------------------------------------------------------------------------

## 2. File Overview

  Metric                                          Result
  -------------------------------------------- ---------
  Rows                                            59,519
  Columns                                             10
  File format                                        CSV
  Earliest `Period` value                        1960.01
  Latest `Period` value                          2026.06
  Exact duplicate rows                                 0
  Duplicate `Series_reference + Period` keys           0
  `Subject` values                                     1
  `UNITS` values                                       3
  `STATUS` values                                      2

The source contains multiple statistical concepts in a single
long-format table.

------------------------------------------------------------------------

## 3. Source Columns

The CSV contains the following columns:

``` text
Series_reference
Period
Data_value
STATUS
UNITS
Subject
Group
Series_title_1
Series_title_2
Series_title_3
```

### Column profile

  -------------------------------------------------------------------------
  Column                  Observed role             MVP treatment
  ----------------------- ------------------------- -----------------------
  `Series_reference`      Stats NZ series           Retain
                          identifier                

  `Period`                Monthly observation       Parse into date/month
                          period                    

  `Data_value`            Observation value         Retain as numeric
                                                    measure

  `STATUS`                Observation status        Retain

  `UNITS`                 Unit of observation       Retain

  `Subject`               Statistical subject       Retain in RAW/staging

  `Group`                 Dataset/classification    Retain
                          group                     

  `Series_title_1`        Primary                   Retain
                          series/product/category   
                          description               

  `Series_title_2`        Additional series         Retain in RAW
                          descriptor                

  `Series_title_3`        Additional series         Retain in RAW
                          descriptor                
  -------------------------------------------------------------------------

------------------------------------------------------------------------

## 4. Null Profile

The source contains:

  Column                 Null count
  -------------------- ------------
  `Series_reference`              0
  `Period`                        0
  `Data_value`                   91
  `STATUS`                        0
  `UNITS`                         0
  `Subject`                       0
  `Group`                         0
  `Series_title_1`                0
  `Series_title_2`           57,868
  `Series_title_3`           57,868

The large number of NULL values in `Series_title_2` and `Series_title_3`
is expected for many series because the source does not require all
title levels to be populated.

`Data_value` requires explicit handling in the ingestion and
transformation layers.

------------------------------------------------------------------------

## 5. Status Profile

The source contains:

  STATUS          Rows
  ----------- --------
  `FINAL`       54,635
  `REVISED`      4,884

The presence of `REVISED` observations means that observation status
should be retained rather than discarded during ingestion.

The MVP will preserve the source status in RAW and analytics models
where relevant.

------------------------------------------------------------------------

## 6. Units Profile

The source contains three units:

  Unit        Meaning in source                   Rows
  ----------- ------------------------------- --------
  `Dollars`   Monetary price observation        34,708
  `Index`     Price index observation           23,228
  `Percent`   Percentage-change observation      1,583

This confirms that the CSV contains multiple business concepts and that
`UNITS` is an important discriminator.

The project must not combine these values into a single generic "price"
measure.

------------------------------------------------------------------------

## 7. Group Profile

The major groups in the source are:

  -----------------------------------------------------------------------
  Group                                                              Rows
  ------------------------------ ----------------------------------------
  Food Price Index Selected                                        34,708
  Monthly Weighted Average       
  Prices for New Zealand         

  Food Price Index Level 4                                          6,225
  Sections for New Zealand       

  Food Price Index Level 3                                          5,040
  Classes for New Zealand        

  Food Price Index Level 3                                          3,374
  Classes for New Zealand,       
  Seasonally adjusted            

  Food Price Index Level 2                                          2,026
  Subgroups for New Zealand      

  Food Price Index for New                                          1,583
  Zealand, percentage change     

  CPI Level 3 Classes for New                                       1,570
  Zealand                        

  Food Price Index Level 2                                          1,205
  Subgroups for New Zealand,     
  Seasonally adjusted            

  CPI Monthly Rents (Broad                                          1,180
  Regions)                       

  Food Price Index Level 1                                            798
  Groups for New Zealand Monthly 

  CPI Monthly Rents (National)                                        471

  CPI Level 2 Subgroups for New                                       471
  Zealand                        

  CPI Level 6 Items for New                                           362
  Zealand                        

  Food Price Index for New                                            325
  Zealand, seasonally adjusted   

  CPI Level 1 Groups for New                                          181
  Zealand Monthly                
  -----------------------------------------------------------------------

This confirms that the source is broader than the MVP. The project will
select only the relevant Food Price Index groups rather than loading
every group into the analytical model.

------------------------------------------------------------------------

## 8. Dataset A Profile --- Product Prices

### Source group

`Food Price Index Selected Monthly Weighted Average Prices for New Zealand`

### Profile

  Metric                                              Result
  --------------------------------------- ------------------
  Rows                                                34,708
  Product series                                         155
  Unique product titles                                  155
  Period range                              2006.06--2026.06
  Units                                              Dollars
  Missing `Data_value`                                    82
  Duplicate `Series_reference + Period`                    0
  STATUS                                               FINAL

### Product-series structure

Each product is identified by a Stats NZ series reference and product
description.

Examples include:

-   `CPIM.SAP0100` --- Oranges, 1kg
-   `CPIM.SAP0101` --- Bananas, 1kg
-   `CPIM.SAP0102` --- Apples, 1kg
-   `CPIM.SAP0103` --- Kiwifruit, 1kg
-   `CPIM.SAP0110` --- Carrots, 1kg

The complete product catalogue is represented by the source series and
should not be recreated manually.

### Grain

The intended grain is:

> **One product series × one month**

Natural source key:

``` text
Series_reference + Period
```

The profiled source contains no duplicate combinations of these fields.

### Missing values

There are 82 missing `Data_value` observations in the product-price
group.

These records should not be silently converted to zero.

The transformation layer should preserve NULL and document the treatment
of missing observations.

------------------------------------------------------------------------

## 9. Dataset B Profile --- Food Price Index

### Level 1

Source group:

`Food Price Index Level 1 Groups for New Zealand Monthly`

Profile:

  Metric                         Result
  ------------------ ------------------
  Rows                              798
  Series                              1
  Series reference         `CPIM.SE901`
  Series title                     Food
  Units                           Index
  Period range         1960.01--2026.06

This is the overall Food Price Index series.

### Level 2

Source group:

`Food Price Index Level 2 Subgroups for New Zealand`

Profile:

  Metric                     Result
  -------------- ------------------
  Rows                        2,026
  Series                          5
  Units                       Index
  Period range     1966.01--2026.06

Selected series:

  Series reference   Series title
  ------------------ ----------------------------------------
  `CPIM.SE9011`      Fruit and vegetables
  `CPIM.SE9012`      Meat, poultry and fish
  `CPIM.SE9013`      Grocery food
  `CPIM.SE9014`      Non-alcoholic beverages
  `CPIM.SE9015`      Restaurant meals and ready-to-eat food

The selected Level 1 and Level 2 series have no duplicate
`Series_reference + Period` combinations in the profiled source.

------------------------------------------------------------------------

## 10. Percentage-Change Profile

### Source group

`Food Price Index for New Zealand, percentage change`

Profile:

  Metric                     Result
  -------------- ------------------
  Rows                        1,583
  Series                          2
  Units                     Percent
  Period range     1960.02--2026.06

Series:

  Series reference   Series title
  ------------------ --------------
  `CPIM.SE901AC`     Food
  `CPIM.SE901PC`     Food

The project recognises these as source-provided percentage-change
observations.

For the MVP, percentage changes will generally be calculated from the
selected monthly price/index observations rather than modelled as a
separate primary fact table. The source percentage-change series can be
retained for validation.

------------------------------------------------------------------------

## 11. Time Period Considerations

The source represents monthly periods using values such as:

``` text
2024.01
2024.02
2024.1
2024.11
2024.12
```

These values represent year and month, not decimal fractions of a year.

Therefore:

``` text
2024.1  -> January 2024
2024.10 -> October 2024
```

The ingestion process must not treat `Period` as a normal floating-point
number.

Recommended transformation:

``` text
raw Period
    |
    v
extract year + month
    |
    v
construct first day of month
    |
    v
DATE
```

Example analytical representation:

``` text
2024.01 -> 2024-01-01
2024.06 -> 2024-06-01
2024.12 -> 2024-12-01
```

------------------------------------------------------------------------

## 12. Source Structure and Modelling Implications

The profiling shows that the CSV is a long-format statistical dataset
rather than a traditional product master.

The same table contains:

``` text
Product prices
    +
Price indexes
    +
Percentage changes
    +
Multiple classification levels
```

Therefore the warehouse should not create one generic fact table
containing all observations.

Instead, the MVP will separate the business concepts:

``` text
                    RAW
                     |
          Selected Price Indexes
                     |
          +----------+----------+
          |                     |
          v                     v
   Product Price          Price Index
      series                 series
          |                     |
          v                     v
fact_product_price      fact_price_index
```

------------------------------------------------------------------------

## 13. Initial Analytical Grain

### `fact_product_price`

``` text
One product series × one month
```

Key:

``` text
Series_reference + Period
```

Measure:

``` text
Data_value
```

Expected unit:

``` text
Dollars
```

### `fact_price_index`

``` text
One Food Price Index series × one month
```

Key:

``` text
Series_reference + Period
```

Measure:

``` text
Data_value
```

Expected unit:

``` text
Index
```

### Percentage change

Percentage changes can be calculated from the relevant observations:

``` text
(current_value - previous_value)
--------------------------------- × 100
       previous_value
```

The exact calculation will depend on the analytical question and whether
monthly or annual change is required.

------------------------------------------------------------------------

## 14. Data Quality Observations

The initial profiling identified the following points that must be
addressed in the pipeline:

1.  `Data_value` contains 91 NULL values.
2.  `STATUS` contains both `FINAL` and `REVISED`.
3.  `UNITS` contains multiple measurement concepts.
4.  `Period` requires careful parsing.
5.  `Series_title_2` and `Series_title_3` contain many NULL values.
6.  The source contains multiple classification levels and statistical
    concepts.
7.  Product-price observations contain 155 distinct product series.
8.  No duplicate `Series_reference + Period` combinations were found in
    the source file.

These observations will directly inform Python validation and dbt tests.

------------------------------------------------------------------------

## 15. MVP Selection

The MVP will use:

### Product Price

``` text
Group =
Food Price Index Selected Monthly Weighted Average Prices for New Zealand

UNITS =
Dollars
```

All 155 product series in this group are in scope for the MVP
product-price dataset.

### Food Price Index

Use:

``` text
Level 1:
CPIM.SE901 — Food

Level 2:
CPIM.SE9011 — Fruit and vegetables
CPIM.SE9012 — Meat, poultry and fish
CPIM.SE9013 — Grocery food
CPIM.SE9014 — Non-alcoholic beverages
CPIM.SE9015 — Restaurant meals and ready-to-eat food
```

### Out of MVP

The following are available but are not required for the first
implementation:

-   Food Price Index Level 3 classes
-   Food Price Index Level 4 sections
-   seasonally adjusted Food Price Index series
-   CPI rent series
-   non-food CPI groups
-   percentage-change series as a separate fact table

They may be added later if they provide clear analytical value.

------------------------------------------------------------------------

## 16. Profiling Conclusion

The source is suitable for the MVP.

The most important modelling conclusion is that the CSV contains
multiple measurement concepts. `UNITS` and `Group` must therefore be
used during source filtering and transformation.

The MVP can now proceed to the ingestion stage with a clear definition
of:

-   source
-   selected groups
-   selected series
-   fields
-   data grain
-   time representation
-   known data-quality issues

The next technical step is:

``` text
Stats NZ CSV
    |
    v
Python ingestion + validation
    |
    v
Snowflake RAW
```
