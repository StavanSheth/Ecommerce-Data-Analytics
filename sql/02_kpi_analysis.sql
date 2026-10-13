-- ==============================================================================
-- BABY EXPLANATION:
-- SQL is like talking to a digital shopkeeper!
-- You ask questions like:
--   "How much money did we make in total?"
--   "Which toys sold the most?"
--   "Which countries spent the most cash?"
-- Let's see how each query answers these questions step-by-step.
-- ==============================================================================


-- ------------------------------------------------------------------------------
-- QUERY 1: Big Overall Store Performance (How did our store do in total?)
--
-- We use "WITH sales AS (...)" as a temporary scratchpad:
-- We only pick rows where:
--   1. is_cancelled = 0 (Nobody returned it)
--   2. Quantity > 0 (Real positive items bought)
--   3. UnitPrice > 0 (Real money spent)
-- Then we calculate:
--   - Total revenue ($)
--   - Total units sold
--   - Distinct invoices (How many separate receipts)
--   - Identified customers (How many known buyers)
-- ------------------------------------------------------------------------------
WITH sales AS (
    SELECT 
        *, 
        Quantity * UnitPrice AS revenue 
    FROM online_retail
    WHERE COALESCE(is_cancelled, 0) = 0 
      AND Quantity > 0 
      AND UnitPrice > 0
)
SELECT 
    ROUND(SUM(revenue), 2) AS revenue,                       -- All money added together
    SUM(Quantity) AS units_sold,                             -- Total number of items bagged
    COUNT(DISTINCT InvoiceNo) AS invoices,                   -- How many shopping trips
    COUNT(DISTINCT CustomerID) AS identified_customers       -- How many different shoppers
FROM sales;


-- ------------------------------------------------------------------------------
-- QUERY 2: Monthly Trends (Did we make more money in December than January?)
--
-- "substr(InvoiceDate, 1, 7)" chops the date to just Year-Month (e.g. "2011-01").
-- Then we group our sales into monthly piles and see earnings month-by-month.
-- ------------------------------------------------------------------------------
SELECT 
    substr(InvoiceDate, 1, 7) AS month,                      -- e.g. "2011-01", "2011-02"
    ROUND(SUM(Quantity * UnitPrice), 2) AS revenue,          -- Total earnings that month
    COUNT(DISTINCT InvoiceNo) AS invoices,                   -- How many receipts that month
    COUNT(DISTINCT CustomerID) AS customers                  -- How many customers visited
FROM online_retail 
WHERE COALESCE(is_cancelled, 0) = 0 
  AND Quantity > 0 
  AND UnitPrice > 0
GROUP BY substr(InvoiceDate, 1, 7)                           -- Put into monthly piles
ORDER BY month;                                              -- Oldest month to newest month


-- ------------------------------------------------------------------------------
-- QUERY 3: Top 20 Best-Selling Products (Our superstar items!)
--
-- We group sales by product code and description, add up all money earned,
-- and show the TOP 20 items bringing in the highest revenue.
-- ------------------------------------------------------------------------------
SELECT 
    StockCode,                                               -- Unique item code
    Description,                                             -- Item name
    ROUND(SUM(Quantity * UnitPrice), 2) AS revenue,          -- Total dollars made by this item
    SUM(Quantity) AS units_sold,                             -- How many units left the shelves
    COUNT(DISTINCT InvoiceNo) AS invoices                    -- In how many baskets it appeared
FROM online_retail 
WHERE COALESCE(is_cancelled, 0) = 0 
  AND Quantity > 0 
  AND UnitPrice > 0
GROUP BY StockCode, Description                              -- Group by product item
ORDER BY revenue DESC                                        -- Put biggest moneymakers first!
LIMIT 20;                                                    -- Only show the Top 20 winners


-- ------------------------------------------------------------------------------
-- QUERY 4: Country Comparison (Which countries love our shop the most?)
--
-- We group sales by Country to see where international orders come from.
-- (Spoiler: The UK is #1, followed by EIRE, Germany, France, etc.)
-- ------------------------------------------------------------------------------
SELECT 
    Country,                                                 -- Country name
    ROUND(SUM(Quantity * UnitPrice), 2) AS revenue,          -- Revenue from this country
    COUNT(DISTINCT InvoiceNo) AS invoices,                   -- Number of orders placed
    COUNT(DISTINCT CustomerID) AS customers                  -- Number of customers in that country
FROM online_retail 
WHERE COALESCE(is_cancelled, 0) = 0 
  AND Quantity > 0 
  AND UnitPrice > 0
GROUP BY Country                                             -- Group into country piles
ORDER BY revenue DESC;                                       -- Most profitable country on top!


-- ------------------------------------------------------------------------------
-- QUERY 5: Repeat Customers vs One-Time Shoppers
--
-- Do people come back to our store, or do they only buy once and leave forever?
-- Step 1: Count how many orders each customer placed.
-- Step 2: If order count = 1, label them '1 order'.
--         If order count > 1, label them '2+ orders' (Repeat customer!).
-- ------------------------------------------------------------------------------
WITH sales AS (
    -- Scratchpad note 1: Find all valid non-cancelled sales
    SELECT * 
    FROM online_retail 
    WHERE COALESCE(is_cancelled, 0) = 0 
      AND Quantity > 0 
      AND UnitPrice > 0
),
customer_orders AS (
    -- Scratchpad note 2: Count how many separate receipts each customer has
    SELECT 
        CustomerID, 
        COUNT(DISTINCT InvoiceNo) AS invoice_count
    FROM sales 
    WHERE CustomerID IS NOT NULL 
    GROUP BY CustomerID
)
SELECT 
    CASE 
        WHEN invoice_count = 1 THEN '1 order' 
        ELSE '2+ orders' 
    END AS purchase_group,                                   -- '1 order' or '2+ orders'
    COUNT(*) AS customers                                    -- Total shoppers in each group
FROM customer_orders 
GROUP BY purchase_group;
