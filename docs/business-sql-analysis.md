# Business SQL Analysis

## 1. Purpose

This document summarizes business-oriented analysis performed using the
analytics-ready data model.

The analysis uses the following models:

- `dim_date`
- `dim_product`
- `fact_product_price`
- `fact_price_index`

The SQL queries used to produce these analyses are stored separately in
`docs/sql/`.

---

## 2. Product Price Trend

### Business Question

How has the price of `Oranges, 1kg` changed over time?

### Analysis

Monthly weighted-average prices for `Oranges, 1kg` were analysed using the
product price fact table together with the date and product dimensions.

### Key Findings

- The available observations cover June 2006 to June 2026.
- The data is stored at monthly grain.
- Prices are recorded in `Dollars`.
- The observations in the analysed result are marked as `FINAL`.
- The price was `$3.11` in June 2006.
- The price was `$5.77` in June 2026.
- The product shows noticeable month-to-month fluctuations over the
  available period.

### Business Insight

The long-term series shows that the price of `Oranges, 1kg` has increased
between the beginning and end of the available period, while also showing
substantial shorter-term fluctuations.

This demonstrates how the platform can support product-level price trend
analysis over time.

---

## 3. Average Product Prices

### Business Question

Which products have the highest average monthly prices?

### Analysis

Average prices were calculated across the available monthly observations
for each product.

### Top 10 Products by Average Price

| Rank | Product | Average Price |
| ---: | --- | ---: |
| 1 | Fresh fish, 1kg | $32.82 |
| 2 | Beef steak - porterhouse/sirloin, 1kg | $28.56 |
| 3 | Infant formula, 900g | $20.04 |
| 4 | Beef steak - blade, 1kg | $17.79 |
| 5 | Prawns, frozen, 700g | $17.46 |
| 6 | Pork - loin chops, 1kg | $15.96 |
| 7 | Roasting lamb and hogget, fresh, chilled or frozen, 1kg | $15.87 |
| 8 | Lamb - chops, 1kg | $15.54 |
| 9 | Chicken breast, 1kg | $14.54 |
| 10 | Beef - mince, 1kg | $14.35 |

### Business Insight

`Fresh fish, 1kg` has the highest average monthly price among the products
included in the analysis, followed by `Beef steak - porterhouse/sirloin, 1kg`.

The result provides a high-level comparison of average product price levels
across the selected dataset.

The averages cover the available observations for each product and should
not be interpreted as current prices.

---

## 4. Monthly Price Changes

### Business Question

Which products experienced the largest month-over-month price increases?

### Analysis

Monthly price changes were calculated by comparing each product's price
with its previous available month using the product-specific time series.

### Largest Observed Monthly Increases

| Date | Product | Price | Previous Price | Price Change |
| --- | --- | ---: | ---: | ---: |
| 2019-03 | Avocado, 1kg | $21.46 | $9.03 | +$12.43 |
| 2023-06 | Capsicums, green, else red, 1kg | $27.18 | $15.84 | +$11.34 |
| 2025-06 | Capsicums, green, else red, 1kg | $25.27 | $14.86 | +$10.41 |
| 2018-09 | Courgettes, 1kg | $20.64 | $10.27 | +$10.37 |
| 2013-09 | Courgettes, 1kg | $18.43 | $8.28 | +$10.15 |

### Business Insight

The largest observed absolute month-over-month increase was recorded for
`Avocado, 1kg` in March 2019, with an increase of `$12.43`.

Several of the largest increases occurred among fruit and vegetable
products, including capsicums, courgettes, beans, avocado, and cucumber.

This analysis measures absolute dollar changes. It does not measure
percentage changes or overall price volatility.

---

## 5. Price Index Trend

### Business Question

How has the selected price index changed over time?

### Analysis

The `CPIM.SE901` price index series was analysed using monthly observations
from the price index fact table.

### Key Findings

- The available series covers January 1960 to June 2026.
- The index reached `1,000` in June 2017.
- The index reached `1,380` in June 2026.
- The index increased by approximately 38% from June 2017 to June 2026.
- The index was `1,341` in December 2025 and `1,380` in June 2026.
- The observations use `Index` units.

### Business Insight

The selected price index shows a substantial long-term increase in the
underlying price level represented by the series.

The index is appropriate for analysing relative changes in a price level over
time rather than comparing absolute dollar prices.

---

## 6. Product Price vs Price Index

### Business Question

Does the price of `Oranges, 1kg` move in the same direction as the selected
price index?

### Analysis

Monthly changes in the `Oranges, 1kg` price were compared with monthly changes
in the `CPIM.SE901` price index.

The comparison focuses on the direction and magnitude of monthly movement
rather than comparing the absolute values of the two measures.

### Examples

| Date | Orange Price Change | Index Change |
| --- | ---: | ---: |
| 2024-06 | -$1.89 | +13 |
| 2024-10 | +$0.59 | -12 |
| 2026-01 | +$0.64 | +28 |
| 2026-06 | -$0.84 | +8 |

### Business Insight

The selected product price and price index do not move in the same direction
every month.

For example:

- In June 2024, the orange price decreased while the index increased.
- In October 2024, the orange price increased while the index decreased.
- In January 2026, both measures increased.
- In June 2026, the orange price decreased while the index increased.

This indicates that individual product prices can fluctuate independently of
the broader price index at the monthly level.

The comparison should not be interpreted as a causal relationship.

---

## 7. Summary of Business Analysis

The analysis demonstrates several ways the analytics-ready data model can
support business questions:

| Analysis | Business Question | Main Technique |
| --- | --- | --- |
| Product Price Trend | How has a product price changed over time? | Time-series analysis |
| Average Product Prices | Which products have the highest average prices? | Aggregation |
| Monthly Price Changes | Which products had the largest monthly increases? | Window function |
| Price Index Trend | How has the price index changed over time? | Time-series analysis |
| Price vs Price Index | Do product prices move with the broader index? | Comparative analysis |

These analyses demonstrate the use of the analytics layer for both
product-level and broader price-level analysis while keeping monetary prices
and index values as separate business concepts.
