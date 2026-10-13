# Power BI dashboard specification

## Data source
Run `src/analyze.py`. Import `sales_transactions.csv`, `monthly_sales.csv`, `country_summary.csv`, `top_products.csv`, `customer_rfm.csv`, and `overall_kpis.csv` as separate tables. Set date fields to Date/DateTime and revenue to currency. Create relationships only where keys are unique and appropriate; do not join fact tables together without a dimensional model.

## Page 1 — Commercial overview
- KPI cards: Revenue, Units Sold, Orders, Identified Customers, Average Order Value
- Monthly revenue trend
- Revenue by country
- Slicers: Country, month, product

## Page 2 — Product performance
- Top 20 products by revenue
- Units sold vs revenue scatter chart
- Product table with revenue, units and invoice count

## Page 3 — Customer retention
- Customer frequency distribution
- RFM score/segment table
- Repeat customer rate and revenue by customer segment

## Page 4 — Data quality
- Missingness from `data_quality.csv`
- Cancelled invoice count, duplicate rows removed and valid sales lines from `overall_kpis.csv`

## Definitions
Revenue excludes cancelled invoice lines, non-positive quantities and non-positive unit prices. Customer metrics count only non-null CustomerID values. RFM is a relative descriptive segmentation, not a lifetime-value forecast.
