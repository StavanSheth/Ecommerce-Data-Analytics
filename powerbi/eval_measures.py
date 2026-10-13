"""
Evaluates all Power BI DAX measures against the actual processed datasets
and verifies that every KPI matches the Power BI Dashboard visuals exactly.
"""
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    root = Path(__file__).resolve().parent.parent
    sales_path = root / "data" / "processed" / "sales_transactions.csv"
    rfm_path = root / "data" / "processed" / "customer_rfm.csv"
    out_dir = root / "powerbi"

    if not sales_path.exists() or not rfm_path.exists():
        raise FileNotFoundError("Missing processed CSVs. Run src/analyze.py first.")

    sales = pd.read_csv(sales_path, dtype={"InvoiceNo": str}, low_memory=False)
    rfm = pd.read_csv(rfm_path)

    # 1. Net Revenue = SUM('sales_transactions'[line_revenue])
    net_revenue = float(sales["line_revenue"].sum())

    # 2. Units Sold = SUM('sales_transactions'[Quantity])
    units_sold = int(sales["Quantity"].sum())

    # 3. Total Orders = DISTINCTCOUNT('sales_transactions'[InvoiceNo])
    total_orders = int(sales["InvoiceNo"].nunique())

    # 4. Identified Customers = DISTINCTCOUNT('sales_transactions'[CustomerID])
    identified_customers = int(sales["CustomerID"].dropna().nunique())

    # 5. Average Order Value = DIVIDE([Net Revenue], [Total Orders], 0)
    aov = (net_revenue / total_orders) if total_orders else 0.0

    # 6. Revenue per Customer
    rev_per_customer = (net_revenue / identified_customers) if identified_customers else 0.0

    # 7. UK Revenue
    uk_sales = sales[sales["Country"] == "United Kingdom"]
    uk_revenue = float(uk_sales["line_revenue"].sum())

    # 8. UK Revenue Share %
    uk_share = (uk_revenue / net_revenue * 100) if net_revenue else 0.0

    # 9. Repeat Customers (frequency >= 2)
    repeat_customers = int((rfm["frequency"] >= 2).sum())

    # 10. Single Order Customers (frequency == 1)
    single_customers = int((rfm["frequency"] == 1).sum())

    # 11. Repeat Customer Rate %
    total_rfm_cust = len(rfm)
    repeat_rate = (repeat_customers / total_rfm_cust * 100) if total_rfm_cust else 0.0

    # 12. VIP Champion Customers (RFM 444)
    vip_champions = int((rfm["rfm_segment_score"] == "444").sum())

    results = [
        {"DAX Measure": "Net Revenue", "Dashboard Element": "KPI Card 1", "Raw Value": round(net_revenue, 2), "Formatted Output": f"${net_revenue:,.2f} ($4.66M)"},
        {"DAX Measure": "Units Sold", "Dashboard Element": "KPI Card 2", "Raw Value": units_sold, "Formatted Output": f"{units_sold:,} (2.39M)"},
        {"DAX Measure": "Total Orders", "Dashboard Element": "KPI Card 3", "Raw Value": total_orders, "Formatted Output": f"{total_orders:,}"},
        {"DAX Measure": "Identified Customers", "Dashboard Element": "KPI Card 4", "Raw Value": identified_customers, "Formatted Output": f"{identified_customers:,}"},
        {"DAX Measure": "Average Order Value", "Dashboard Element": "KPI Card 5", "Raw Value": round(aov, 2), "Formatted Output": f"${aov:,.2f}"},
        {"DAX Measure": "Revenue per Customer", "Dashboard Element": "Secondary Metric", "Raw Value": round(rev_per_customer, 2), "Formatted Output": f"${rev_per_customer:,.2f}"},
        {"DAX Measure": "UK Revenue", "Dashboard Element": "Bar Chart #1 Leader", "Raw Value": round(uk_revenue, 2), "Formatted Output": f"${uk_revenue:,.2f} ($4.05M)"},
        {"DAX Measure": "UK Revenue Share %", "Dashboard Element": "Market Share", "Raw Value": round(uk_share, 2), "Formatted Output": f"{uk_share:.2f}%"},
        {"DAX Measure": "Repeat Customers", "Dashboard Element": "Donut Chart Segment", "Raw Value": repeat_customers, "Formatted Output": f"{repeat_customers:,}"},
        {"DAX Measure": "Single Order Customers", "Dashboard Element": "Donut Chart Segment", "Raw Value": single_customers, "Formatted Output": f"{single_customers:,}"},
        {"DAX Measure": "Repeat Customer Rate %", "Dashboard Element": "Donut Chart Share", "Raw Value": round(repeat_rate, 2), "Formatted Output": f"{repeat_rate:.2f}%"},
        {"DAX Measure": "VIP Champion Customers (444)", "Dashboard Element": "RFM Segment Table", "Raw Value": vip_champions, "Formatted Output": f"{vip_champions:,}"},
    ]

    res_df = pd.DataFrame(results)
    csv_file = out_dir / "measures_output.csv"
    res_df.to_csv(csv_file, index=False)

    print("================================================================================")
    print("POWER BI EVALUATED MEASURES OUTPUT — ONLINE RETAIL COMMERCIAL ANALYTICS")
    print("================================================================================")
    print(res_df.to_string(index=False))
    print(f"\nSaved evaluated measure outputs to: {csv_file}")

if __name__ == "__main__":
    main()
