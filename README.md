FUTURE_DS_01: Business Sales Performance Analytics

**Internship:** Future Interns, Data Science & Analytics, Task 1
**Author:** B. Devi
**Tools:** Python (pandas, matplotlib, scipy), Microsoft Excel

## Objective
Analyse Trendora's sales data to find revenue trends, top-selling products, high-value categories and regional performance, and turn them into actionable recommendations.

> **Note on data:** the dataset is synthetic (created for learning, per its data dictionary). The analysis demonstrates the method; the numbers do not describe a real business.

## Approach
1. **Clean** the raw data (5 duplicates, 5 missing discounts, 2 inconsistent state names, 8 region/state mismatches, text dates). Full details: [`docs/Data_Cleaning_Log.md`](docs/Data_Cleaning_Log.md)
2. **Define KPIs on a net basis:** Returned and Cancelled orders (7.9%) earn no revenue, so headline figures use Delivered orders only; gross figures are shown for reference.
3. **Analyse in Python** (`trendora_analysis.py`): trends, category, region, state, product, discount and returns analysis, plus chi-square tests to avoid over-reading small differences.
4. **Build an interactive Excel dashboard** with filters for date range, region, category, payment mode and order basis.
5. **Write insights and recommendations:** [`Insights_and_Recommendations.md`](Insights_and_Recommendations.md)

## Key results (net, delivered orders)
| KPI | Value |
|---|---|
| Net sales | ₹29.47 L (gross ₹32.18 L) |
| Net profit | ₹11.44 L (38.8% margin) |
| Delivered orders | 1,105 of 1,200 |
| Avg order value | ₹2,667 |
| Returned + Cancelled | 7.9% of orders (₹2.71 L sales lost) |

**Highlights**
- Sales are flat year on year (+1.0%); Q4 is the only season that repeats in both years.
- Clothing is 49% of sales; South is the top region (29.5%); Central is the weakest (9.5%).
- Deeper discounts cut margin (44.7% at 0% to 25.5% at 25%) without raising units per order.
- Three top sellers (Printed Saree, Lightweight Jacket, Running Sneakers) earn only 34–36% margin versus 38.8% overall.

![Dashboard](dashboard/dashboard_screenshot.png)

![Monthly trend](charts/1_monthly_trend.png)
![Discount vs margin and quantity](charts/6_discount_margin_vs_quantity.png)
![Region](charts/3_region.png)
![Top products](charts/4_top_products.png)

## Repository structure
```
FUTURE_DS_01/
├── README.md
├── Insights_and_Recommendations.md
├── trendora_analysis.py
├── requirements.txt
├── data/
│   ├── Trendora_Sales_Raw.csv
│   └── Trendora_Sales_Cleaned.csv
├── charts/                  (PNG charts from Python)
├── dashboard/
│   └── Trendora_Sales_Dashboard.xlsx
└── docs/
    └── Data_Cleaning_Log.md
```

## How to run
```bash
pip install -r requirements.txt
python trendora_analysis.py
```
The script prints the KPI summary and regenerates all charts in `charts/`.

## Using the Excel dashboard
Open `dashboard/Trendora_Sales_Dashboard.xlsx` in Excel and use the yellow dropdowns on the **Dashboard** sheet. Every KPI and chart updates automatically. *Order Basis* = "Delivered only" (default, net) or "All orders" (gross). The **Calc** sheet holds the formulas feeding the charts; **Data** holds the cleaned dataset.
