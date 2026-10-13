from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import numpy as np

# ==============================================================================
# BABY EXPLANATION:
# Imagine you are running an online toy shop!
# Every time someone buys a teddy bear or returns a toy, a line is written
# on a digital receipt.
# This script reads thousands of receipts, throws away junk/duplicates,
# separates normal sales from cancelled orders, figures out who your best
# customers are (RFM scoring), and shows which toys and countries bring in
# the most money!
# ==============================================================================

# This is our "Shopping List" / Checklist of columns that MUST exist on the receipt:
REQUIRED = [
    "InvoiceNo",    # Receipt number (e.g. "536365"; if it starts with "C", it means Cancelled!)
    "StockCode",    # Toy/Product ID number (e.g. "85123A")
    "Description",  # Name of the toy (e.g. "White Hanging Heart T-Light Holder")
    "Quantity",     # How many items were bought (e.g. 6 items)
    "InvoiceDate",  # Date and time the purchase happened (e.g. "12/1/2010 8:26")
    "UnitPrice",    # Price of ONE single item in dollars/pounds (e.g. $2.55)
    "CustomerID",   # The secret ID number of the shopper (e.g. 17850)
    "Country"       # The country where the buyer lives (e.g. "United Kingdom")
]


def main() -> None:
    # -------------------------------------------------------------------------
    # STEP 1: Get the file paths from the user
    # -------------------------------------------------------------------------
    # We ask: "Where is the raw CSV file?" and "Where do you want the final reports?"
    p = argparse.ArgumentParser(description="Analyze the Online Retail transaction dataset")
    p.add_argument("--input", required=True, help="Path to online_retail.csv")
    p.add_argument("--output", default="data/processed", help="Output directory")
    args = p.parse_args()

    # Make the destination folder if it doesn't exist yet
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # STEP 2: Read the raw CSV file
    # -------------------------------------------------------------------------
    # pd.read_csv loads the file like an Excel sheet into memory.
    # encoding_errors="replace" ensures strange symbols don't crash our script.
    df = pd.read_csv(args.input, encoding_errors="replace")

    # Check our checklist: are any required columns missing?
    missing_cols = sorted(set(REQUIRED) - set(df.columns))
    if missing_cols:
        raise SystemExit(f"Input schema mismatch; missing columns: {missing_cols}")

    # -------------------------------------------------------------------------
    # STEP 3: Data Quality Check (Health checkup)
    # -------------------------------------------------------------------------
    # Count missing values, null percentages, and unique items across every column.
    quality = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "missing_count": [int(df[c].isna().sum()) for c in df.columns],
        "missing_pct": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
        "unique_values": [int(df[c].nunique(dropna=True)) for c in df.columns]
    })
    quality.to_csv(out / "data_quality.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 4: Remove exact twin duplicates
    # -------------------------------------------------------------------------
    # If the exact same line was entered twice by mistake, drop the duplicate copy.
    original_rows = len(df)
    df = df.drop_duplicates().copy()

    # -------------------------------------------------------------------------
    # STEP 5: Convert columns into their proper formats (Types)
    # -------------------------------------------------------------------------
    # Turn text dates ("12/1/2010") into real Python calendar dates
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce", dayfirst=True)

    # Make sure numbers are treated as numbers, not words
    for c in ["Quantity", "UnitPrice", "CustomerID"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Clean invoice numbers (strip accidental spaces around text)
    df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()

    # If the invoice number begins with 'C' (like "C536379"), this order was CANCELLED!
    df["is_cancelled"] = df["InvoiceNo"].str.upper().str.startswith("C", na=False)

    # Total money for this line = How many items * Price per item
    # (e.g. 3 teddy bears * $10 each = $30 line revenue)
    df["line_revenue"] = df["Quantity"] * df["UnitPrice"]

    # Save the cleaned dataset (retaining cancellations flagged for reference)
    df.to_csv(out / "online_retail_clean.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 6: Filter for VALID, REAL SALES
    # -------------------------------------------------------------------------
    # For business earnings reports, we only want real positive sales:
    # - NOT cancelled
    # - Quantity > 0 (they actually bought items)
    # - UnitPrice > 0 (the item wasn't free / damaged / zero price)
    # - Valid date recorded
    sales = df[
        (~df["is_cancelled"]) & 
        (df["Quantity"] > 0) & 
        (df["UnitPrice"] > 0) & 
        df["InvoiceDate"].notna()
    ].copy()

    # Add a 'month' column (e.g. "2011-01") so we can group sales month by month
    sales["month"] = sales["InvoiceDate"].dt.to_period("M").astype(str)
    sales.to_csv(out / "sales_transactions.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 7: Monthly Sales Summary
    # -------------------------------------------------------------------------
    # Group by month and calculate:
    # - Total revenue made
    # - Total units/items sold
    # - How many receipts/invoices
    # - How many unique customers bought something
    monthly = sales.groupby("month", as_index=False).agg(
        revenue=("line_revenue", "sum"),
        units_sold=("Quantity", "sum"),
        invoices=("InvoiceNo", "nunique"),
        unique_customers=("CustomerID", "nunique")
    )
    monthly.to_csv(out / "monthly_sales.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 8: Country Summary (Who bought the most globally?)
    # -------------------------------------------------------------------------
    country = sales.groupby("Country", dropna=False, as_index=False).agg(
        revenue=("line_revenue", "sum"),
        units_sold=("Quantity", "sum"),
        invoices=("InvoiceNo", "nunique"),
        customers=("CustomerID", "nunique")
    ).sort_values("revenue", ascending=False)
    country.to_csv(out / "country_summary.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 9: Top Products (What are our best-selling items?)
    # -------------------------------------------------------------------------
    product = sales.groupby(["StockCode", "Description"], dropna=False, as_index=False).agg(
        revenue=("line_revenue", "sum"),
        units_sold=("Quantity", "sum"),
        invoices=("InvoiceNo", "nunique")
    ).sort_values("revenue", ascending=False)
    product.to_csv(out / "top_products.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 10: RFM Customer Analysis (Finding our VIP best friends!)
    # -------------------------------------------------------------------------
    # RFM stands for:
    # - R = Recency: Did they buy recently, or a year ago? (Recent = Better!)
    # - F = Frequency: Do they buy often, or just once? (Often = Better!)
    # - M = Monetary: Did they spend lots of money? (More = Better!)
    customer_sales = sales.dropna(subset=["CustomerID"]).copy()
    if len(customer_sales):
        # Reference date: The day after the latest transaction in our dataset
        ref = customer_sales["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)

        # Calculate R, F, M for each customer:
        rfm = customer_sales.groupby("CustomerID").agg(
            last_purchase=("InvoiceDate", "max"),
            frequency=("InvoiceNo", "nunique"),
            monetary=("line_revenue", "sum")
        ).reset_index()

        # How many days since their last visit?
        rfm["recency_days"] = (ref - rfm["last_purchase"].dt.normalize()).dt.days

        # Grade them from 1 (lowest) to 4 (best):
        # R_score: 4 = bought very recently, 1 = bought long ago
        rfm["R_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), 4, labels=[4, 3, 2, 1]).astype(int)
        # F_score: 4 = bought many times, 1 = bought only once
        rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
        # M_score: 4 = spent huge money, 1 = spent very little
        rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)

        # Combine into a 3-digit score like "444" (The ultimate VIP Gold customer!)
        rfm["rfm_segment_score"] = (
            rfm["R_score"].astype(str) + 
            rfm["F_score"].astype(str) + 
            rfm["M_score"].astype(str)
        )
        rfm.to_csv(out / "customer_rfm.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 11: High-Level Overall Business KPIs
    # -------------------------------------------------------------------------
    kpis = pd.DataFrame([{
        "source_rows": original_rows,
        "rows_after_deduplication": len(df),
        "duplicate_rows_removed": original_rows - len(df),
        "valid_sales_lines": len(sales),
        "cancelled_invoice_lines": int(df["is_cancelled"].sum()),
        "net_revenue_valid_sales": round(float(sales["line_revenue"].sum()), 2),
        "units_sold": int(sales["Quantity"].sum()),
        "distinct_invoices": int(sales["InvoiceNo"].nunique()),
        "identified_customers": int(sales["CustomerID"].nunique())
    }])
    kpis.to_csv(out / "overall_kpis.csv", index=False)

    # -------------------------------------------------------------------------
    # STEP 12: Print friendly completion message
    # -------------------------------------------------------------------------
    print(f"Validated input: {args.input}")
    print(f"Rows read: {original_rows}; rows after deduplication: {len(df)}; valid sales lines: {len(sales)}")
    print("Wrote cleaned transactions, data quality and business summaries to:", out.resolve())
    print("Review data_quality.csv and confirm date parsing before interpreting results.")


if __name__ == "__main__":
    main()
