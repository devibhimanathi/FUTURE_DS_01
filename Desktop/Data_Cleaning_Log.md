# Data Cleaning Log

**Source:** synthetic Trendora sales dataset, 1,205 raw rows × 18 columns (`data/Trendora_Sales_Raw.csv`)
**Output:** 1,200 rows × 18 columns, no missing values (`data/Trendora_Sales_Cleaned.csv`)

| # | Issue found | Rows affected | Action |
|---|---|---|---|
| 1 | Exact duplicate rows (same Order_ID and values) | 5 | Removed, leaving 1,200 unique orders |
| 2 | Missing `Discount_Percent` | 5 | Recovered from the identity `Sales_INR = Quantity × Unit_Price_INR × (1 − Discount%)` |
| 3 | Inconsistent text case in `State` ("karnataka", "punjab") | 2 | Standardised to title case |
| 4 | `Region` did not match `State` (e.g. a Karnataka order tagged North, a Punjab order tagged South, Goa tagged Central/North, Gujarat tagged South, Haryana tagged West, Odisha tagged North, Rajasthan tagged South) | 8 | Region re-derived from State using one fixed mapping (South: TN, AP, KA, TS, KL · North: PB, HR, UP, RJ, DL · West: MH, GJ, GA · East: BR, OD, WB, JH · Central: CG, MP) |
| 5 | `Order_Date` stored as text in the cleaned sheet | all | Converted to real dates (range 2024-01-02 to 2025-12-31) |
| 6 | Returned / Cancelled orders counted as revenue | 95 | Kept in the data, but headline KPIs use Delivered orders only ("Net"); the dashboard has an Order Basis switch (Delivered only / All orders) |

## Validation checks (all passed after cleaning)
- `Sales_INR` matches Quantity × Price × (1 − Discount%) on all 1,200 rows
- `Profit_INR` matches Sales − Quantity × Cost on all 1,200 rows
- No negative profit; no duplicate Order_IDs; each Product_ID has one name, price, cost and category
- Dashboard (Excel) totals were reconciled to the pandas results: Net sales ₹29.47 L, profit ₹11.44 L, 1,105 orders

## Known data limitation (not fixed)
`Customer_ID`, `Customer_Name` and `State` are not consistent with each other (20 distinct names across 385 IDs; 308 IDs appear in more than one state), so customer-level analysis was excluded.
