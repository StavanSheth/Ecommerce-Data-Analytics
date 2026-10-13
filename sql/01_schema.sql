-- ==============================================================================
-- BABY EXPLANATION:
-- What is a table? Imagine creating a clean, digital spreadsheet for an online store!
-- Each column holds one specific piece of receipt information:
--   TEXT: words and strings (like "White Lantern" or "United Kingdom")
--   INTEGER: whole numbers (like buying 5 items)
--   REAL: decimal numbers with cents/pence (like $3.50 or $12.99)
-- ==============================================================================

-- Create a table named 'online_retail' if it doesn't already exist.
-- You can load 'online_retail_clean.csv' into this table with any SQL client or SQLite.
CREATE TABLE IF NOT EXISTS online_retail (
    InvoiceNo    TEXT,    -- Receipt number (e.g. "536365" or "C536379" if cancelled)
    StockCode    TEXT,    -- Unique code for the product item (e.g. "85123A")
    Description  TEXT,    -- Name of the item being sold (e.g. "WHITE HEART T-LIGHT HOLDER")
    Quantity     INTEGER, -- How many pieces the customer bought (e.g. 6 items)
    InvoiceDate  TEXT,    -- Date & time when purchased (e.g. "2010-12-01 08:26:00")
    UnitPrice    REAL,    -- Price for one single item (e.g. $2.55)
    CustomerID   REAL,    -- The unique ID number of the buyer (e.g. 17850.0)
    Country      TEXT,    -- The country where the buyer lives (e.g. "United Kingdom")
    is_cancelled INTEGER, -- 1 if order was cancelled/returned, 0 if normal purchase
    line_revenue REAL     -- Total cost for this line: Quantity multiplied by UnitPrice
);

-- ==============================================================================
-- What are INDEXES?
-- Think of an index like bookmarks or an address book!
-- Without an index, the database would have to read every single row one by one.
-- With an index, it jumps directly to the answer in milliseconds!
-- ==============================================================================

-- Index on InvoiceDate: Speeds up looking for sales by year or month
CREATE INDEX IF NOT EXISTS idx_retail_date ON online_retail(InvoiceDate);

-- Index on CustomerID: Speeds up finding what a specific customer bought
CREATE INDEX IF NOT EXISTS idx_retail_customer ON online_retail(CustomerID);

-- Index on StockCode: Speeds up searching for a specific toy or product
CREATE INDEX IF NOT EXISTS idx_retail_product ON online_retail(StockCode);
