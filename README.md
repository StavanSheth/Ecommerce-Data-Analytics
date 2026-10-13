# Online Retail Transaction Analytics

Intermediate-level SQL + Python + Power BI project for revenue, product, geography and repeat-customer analysis.

## Dataset
Download the public UCI Online Retail dataset mirrored on Kaggle: https://www.kaggle.com/datasets/carrie1/ecommerce-data
Place the CSV at `data/raw/online_retail.csv`. Common source columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`. Check the dataset license before redistributing data.

## Run (Python 3.10+)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/analyze.py --input data/raw/online_retail.csv --output data/processed
```
Outputs include cleaned transactions, quality report, monthly sales, country and product summaries, customer RFM segments and top-product tables. Outputs are generated from the actual downloaded file; no metrics are hard-coded.

## SQL
SQL scripts are SQLite-compatible. Load `online_retail_clean.csv` as `online_retail` and run the queries in `sql/`.

## Power BI
Import cleaned output CSVs from `data/processed/`, add measures from `powerbi/measures.dax`, and follow `powerbi/dashboard_spec.md`. A `.pbix` is a Power BI Desktop binary and must be saved from Power BI Desktop; this repository provides source code and build instructions rather than a generated binary.

## Definitions and caveats
Revenue is `Quantity * UnitPrice`; cancelled invoices (invoice numbers beginning with `C`) are excluded from net-sales summaries and reported separately. CustomerID may be missing. RFM scores are descriptive segmentations, not predictions. This is historical transaction data, not necessarily representative of current e-commerce behaviour.
