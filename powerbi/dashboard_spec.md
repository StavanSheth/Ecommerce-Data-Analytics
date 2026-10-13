# Power BI Dashboard Specification — Online Retail & E-Commerce Analytics

This specification details the canvas layout, visual objects, fields, and formatting rules to reproduce the commercial dashboard shown in `powerbi/dashboard_preview.png`.

---

## 1. Canvas Setup & Theme
* **Canvas Size:** 16:9 widescreen (1920 × 1080 px or standard 1280 × 720 px)
* **Background:** Light off-white (`#F8FAFC`)
* **Color Palette:**
  * **Primary Emerald / Teal:** `#0D9488` / `#059669` (Main KPI accent and top country bar)
  * **Slate / Charcoal:** `#1E293B` / `#334155` (Secondary bars and neutral visual elements)
  * **Cards Background:** Pure white (`#FFFFFF`) with rounded corners (4px radius) and subtle drop shadow

---

## 2. Top Header & Slicer Bar
Place at the top of the canvas (`Y: 10px`, `Height: 80px`):
* **Title TextBox:** "Online Retail & E-Commerce Commercial Analytics" (Font: Segoe UI Semibold, 22pt, Emerald `#0D9488`)
* **Dropdown Slicers:**
  1. `sales_transactions[Country]` — Slicer header: "Country" (Default: All)
  2. `sales_transactions[month]` — Slicer header: "Month" (Default: Full Year / All)
  3. `sales_transactions[Description]` — Slicer header: "Product" (Default: All)

---

## 3. KPI Summary Cards (Row 1)
5 single-value Card visuals placed horizontally across the canvas:

| Card Title | DAX Measure | Target Format | Displayed Value (All Data) |
| :--- | :--- | :--- | :--- |
| **Net Revenue** | `[Net Revenue]` | Currency (`$#,##0.00` / `$4.66M`) | `$4.66M` |
| **Units Sold** | `[Units Sold]` | Whole Number (`#,##0` / `2.39M`) | `2.39M` |
| **Total Orders** | `[Total Orders]` | Whole Number (`#,##0`) | `8,556` |
| **Identified Customers** | `[Identified Customers]` | Whole Number (`#,##0`) | `2,997` |
| **Average Order Value** | `[Average Order Value]` | Currency (`$#,##0` or `$#,##0.00`) | `$545` (`$545.03`) |

---

## 4. Visual 1: Monthly Revenue Trend (Area / Line Chart)
* **Visual Type:** Area Chart or Line Chart
* **Position:** Center-Left quadrant (`Width: 50%`, `Height: 380px`)
* **X-Axis:** `monthly_sales[month]` (Sorted chronologically from 2010 to 2011)
* **Y-Axis:** `[Net Revenue]`
* **Fill Color:** Emerald Green gradient fill (`#0D9488` with 20% opacity)
* **Insights:** Highlights consistent baseline transactions throughout early 2011 with massive Q4 holiday acceleration in September, October, and November ($400k+ / month).

---

## 5. Visual 2: Top Countries by Revenue (Horizontal Bar Chart)
* **Visual Type:** Clustered Bar Chart
* **Position:** Center-Right quadrant (`Width: 48%`, `Height: 380px`)
* **Y-Axis:** `country_summary[Country]` (Sorted descending by Revenue)
* **X-Axis:** `[Net Revenue]` (Data Labels: On, Currency in Millions / Thousands)
* **Color Highlights:** Top bar (United Kingdom) highlighted in vibrant Emerald (`#059669`), remaining bars in Slate Blue (`#475569`).
* **Rankings Shown:**
  1. United Kingdom: `$4,052,207` (86.9% of global sales)
  2. EIRE (Ireland): `$102,281`
  3. Germany: `$93,934`
  4. Netherlands: `$89,851`
  5. France: `$85,476`

---

## 6. Visual 3: Customer Retention & Repeat Orders (Donut Chart)
* **Visual Type:** Donut Chart
* **Position:** Bottom-Left quadrant
* **Legend:** `customer_orders[purchase_group]` ("1 Order", "2+ Orders")
* **Values:** `[Identified Customers]`
* **Data Labels:** Category & Percentage of Total
* **Insights:** Shows breakdown of one-time shoppers versus repeat loyal customers who generate recurring transaction volume.

---

## 7. Visual 4: Top Products by Revenue (Table Visual)
* **Visual Type:** Table
* **Position:** Bottom-Right quadrant
* **Columns:**
  * `top_products[Description]` (Product item description)
  * `[Net Revenue]` (Formatted as Currency)
  * `[Units Sold]` (Formatted as Whole Number)
* **Sorting:** `[Net Revenue]` Descending (Top 20 products displayed)

---

## 8. Data Model & Relationships
* **Tables Imported:**
  * `sales_transactions` (Fact table of valid non-cancelled transactions from `data/processed/sales_transactions.csv`)
  * `customer_rfm` (Customer dimension table with RFM scores from `data/processed/customer_rfm.csv`)
  * `monthly_sales` (Aggregated monthly table from `data/processed/monthly_sales.csv`)
  * `country_summary` (Aggregated country table from `data/processed/country_summary.csv`)
  * `top_products` (Aggregated product performance table from `data/processed/top_products.csv`)
* **Relationship:** `sales_transactions[CustomerID]` *(Many)* &rarr; *(1)* `customer_rfm[CustomerID]` (Single direction filter).
