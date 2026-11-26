# Trendora Sales Performance: Insights & Recommendations

**Period:** 2 Jan 2024 – 31 Dec 2025 | **Orders:** 1,200 | **Tools:** Python (pandas, matplotlib, scipy), Microsoft Excel
**Reporting basis:** *Net* = Delivered orders only (1,105 orders). Returned and Cancelled orders earn no revenue, so they are excluded from headline KPIs and shown separately as a loss.

## 1. Headline KPIs
| KPI | Net (Delivered) | Gross (all orders, for reference) |
|---|---|---|
| Sales | **₹29.47 L** | ₹32.18 L |
| Profit | **₹11.44 L** | ₹12.50 L |
| Profit margin | 38.8% | 38.8% |
| Orders | 1,105 | 1,200 |
| Avg order value | ₹2,667 | ₹2,681 |
| Units sold | 2,318 | 2,530 |

**Revenue leakage:** 95 orders (7.9%) were Returned (5.3%, 64 orders) or Cancelled (2.6%, 31 orders). That is ₹2.71 L of sales and ₹1.06 L of profit that never materialised.

## 2. Key Insights (net basis)

**Revenue trend**
- Sales are flat year on year: ₹14.66 L (2024) vs ₹14.81 L (2025), about +1.0%. Profit is flat too (₹5.68 L vs ₹5.76 L). The business is not growing.
- Q4 is the only consistently strong season: 29.8% of annual sales in 2024 and 29.4% in 2025. Peak month is Oct 2024 (₹1.69 L).
- Other dips do not repeat across years. Feb–Mar was strong in 2024 (₹1.32 L, ₹1.39 L) but weak in 2025 (₹0.78 L, ₹0.96 L), so we cannot call it a seasonal low from two years of data.

**Categories and products**
- Clothing drives almost half of revenue (₹14.48 L, 49.1%), then Accessories (22.2%), Footwear (14.8%) and Ethnic Wear (13.8%).
- Top 5 products: Running Sneakers (₹3.33 L), Lightweight Jacket (₹3.03 L), Printed Saree (₹2.88 L), High-Rise Denim Jeans (₹2.43 L), Casual Hoodie (₹2.27 L). Together 47.3% of sales.
- Margins differ a lot by product. Leather Belt (48.9%), Oversized Graphic Tee (46.1%) and Sunglasses (45.2%) earn the most per rupee. Three of the biggest sellers earn well below the 38.8% average: Printed Saree (34.3%), Lightweight Jacket (35.7%) and Running Sneakers (36.1%).

**Regions and states**
- South leads (₹8.68 L, 29.5%), then West (25.4%), North (20.6%), East (15.0%) and Central (9.5%, ₹2.80 L).
- Regional margins are almost identical (38.4% to 39.1%), so regional gaps come from volume, not pricing.
- Top states: Goa (₹2.86 L), Gujarat (₹2.40 L), Andhra Pradesh (₹2.30 L), Maharashtra (₹2.24 L), Telangana (₹1.63 L). Goa ranking first despite being a small state is worth validating with real data.

**Discounts**
- Margin falls as discount rises: 0% → 44.7%, 5% → 41.3%, 10% → 38.6%, 15% → 34.9%, 20% → 31.4%, 25% → 25.5%. This is partly arithmetic (a discount lowers price while cost stays fixed).
- The important finding: bigger discounts do **not** come with bigger baskets. Average units per order is about 2.1 at 0%, 2.1 at 10% and 1.95 at 25% (correlation between discount and quantity: 0.01). Deep discounts cost margin without lifting units per order.
- 34.7% of all orders (416) carry a discount of 15% or more.

**Returns, cancellations and payments**
- Returned 5.3%, Cancelled 2.6%, total 7.9%.
- Credit Card orders show the highest loss rate (11.0%) versus 3.7% for Cash on Delivery. A chi-square test gives p = 0.07, so this is a **directional signal, not statistically proven**.
- Differences by category (Ethnic Wear 9.9% highest) and by region (South 9.1% highest) are **not statistically significant** (p = 0.47 and p = 0.85), so they should not drive targeted action.

## 3. Recommendations
1. **Cap discounts at 15%.** Orders above 15% (the 20% and 25% tiers) show no basket-size benefit and margins of 25–31%. If volume held steady, capping them at 15% would add about ₹31 K profit (2.7% of net profit). Treat this as an upper bound and A/B test it before rolling out.
2. **Push high-margin items.** Bundle or cross-sell Leather Belts, Graphic Tees and Sunglasses with top sellers such as Jackets and Sneakers to raise margin without needing new traffic.
3. **Review pricing and supplier cost of low-margin bestsellers.** Printed Saree, Lightweight Jacket and Running Sneakers sell well but earn 34–36%. Small price or cost changes here move total profit the most.
4. **Plan for Q4.** Build stock and campaigns for Oct–Dec, the only season that repeats in both years. Collect more months of data before declaring any other slow period.
5. **Grow Central and East, protect South and West.** Central and East together give about 25% of sales at the same margins as other regions. Test local campaigns and delivery promises there. Check whether the gap reflects demand or just reach before investing heavily.
6. **Reduce returns and cancellations.** 7.9% of orders cost ₹2.71 L in sales. Start with general measures (clearer size guides and product photos, order confirmation checks) and monitor Credit Card payment failures, since that is the one directional signal.

## 4. Limitations
- **The dataset is synthetic** (created for learning, as stated in its data dictionary). Findings demonstrate the method, not real business performance.
- Only two years of data, so seasonality is based on two cycles.
- No customer acquisition or marketing cost in the data, so recommendations focus on products, discounts and operations.
- Customer-level analysis was **not** done: the same Customer_ID appears under different names and in different states (308 of 385 IDs span more than one state), so repeat-purchase and loyalty conclusions would not be reliable.
- Discount findings show association, not proven cause. An A/B test would confirm the effect on order volume.
- Region was re-derived from State (see `docs/Data_Cleaning_Log.md`).
