"""
FUTURE_DS_01 - Business Sales Performance Analytics (Trendora)
Python analysis: KPIs, charts and statistical checks.

Run:  python trendora_analysis.py
Input : data/Trendora_Sales_Cleaned.csv   (cleaned dataset, 1,200 orders)
Output: charts/*.png and printed KPI summary

Reporting basis: "Net" = Delivered orders only (Returned and Cancelled orders do not
earn revenue). Gross figures (all orders) are shown alongside for reference.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(__file__).parent
CH = ROOT / "charts"; CH.mkdir(exist_ok=True)
df = pd.read_csv(ROOT / "data" / "Trendora_Sales_Cleaned.csv", parse_dates=["Order_Date"])
df["Lost"] = df.Order_Status.isin(["Returned", "Cancelled"])
net = df[~df.Lost].copy()

plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titleweight": "bold", "font.size": 10})
NAVY, GREEN, AMBER, RED, PURPLE = "#2E2A7A", "#10B981", "#E08E0B", "#DC2626", "#6D28D9"

def save(name):
    plt.tight_layout(); plt.savefig(CH / f"{name}.png", dpi=150); plt.close()

def lakh(x): return x / 1e5

# ---------------- KPIs ----------------
k = {
    "Gross sales (all orders), Rs": df.Sales_INR.sum(),
    "Net sales (delivered), Rs": net.Sales_INR.sum(),
    "Net profit (delivered), Rs": net.Profit_INR.sum(),
    "Net profit margin %": net.Profit_INR.sum() / net.Sales_INR.sum() * 100,
    "Delivered orders": len(net),
    "Avg order value (net), Rs": net.Sales_INR.mean(),
    "Units sold (net)": net.Quantity.sum(),
    "Returned %": (df.Order_Status == "Returned").mean() * 100,
    "Cancelled %": (df.Order_Status == "Cancelled").mean() * 100,
    "Sales lost to returns+cancels, Rs": df[df.Lost].Sales_INR.sum(),
    "Profit lost to returns+cancels, Rs": df[df.Lost].Profit_INR.sum(),
}
print("=== KPIs ===")
for a, b in k.items(): print(f"{a:38s}: {b:,.2f}")

# ---------------- Aggregations (net) ----------------
monthly = net.groupby(net.Order_Date.dt.to_period("M")).agg(Sales=("Sales_INR", "sum"), Profit=("Profit_INR", "sum"))
yearly = net.groupby(net.Order_Date.dt.year)[["Sales_INR", "Profit_INR"]].sum()
q = net.groupby([net.Order_Date.dt.year, net.Order_Date.dt.quarter]).Sales_INR.sum().unstack()
cat = net.groupby("Category").agg(S=("Sales_INR", "sum"), P=("Profit_INR", "sum")).sort_values("S")
reg = net.groupby("Region").agg(S=("Sales_INR", "sum"), P=("Profit_INR", "sum"), N=("Order_ID", "count")).sort_values("S")
state = net.groupby("State").Sales_INR.sum().sort_values(ascending=False)
prod = net.groupby("Product_Name").agg(S=("Sales_INR", "sum"), P=("Profit_INR", "sum"))
prod["M"] = prod.P / prod.S * 100
disc = df.groupby("Discount_Percent").agg(S=("Sales_INR", "sum"), P=("Profit_INR", "sum"), N=("Order_ID", "count"), Q=("Quantity", "mean"))
disc["M"] = disc.P / disc.S * 100
pay = df.groupby("Payment_Mode").Lost.agg(["mean", "sum", "count"])

print("\n=== Yearly (net) ===\n", yearly.round(0))
print("YoY sales %:", round((yearly.Sales_INR[2025] / yearly.Sales_INR[2024] - 1) * 100, 2))
print("Quarter share % of year:\n", (q.div(q.sum(1), axis=0) * 100).round(1))
print("Peak month:", monthly.Sales.idxmax(), round(monthly.Sales.max()), "| lowest:", monthly.Sales.idxmin(), round(monthly.Sales.min()))
print("\nCategory share %:", (cat.S / cat.S.sum() * 100).round(1).to_dict())
print("Region share %:", (reg.S / reg.S.sum() * 100).round(1).to_dict(), "| margin %:", (reg.P / reg.S * 100).round(1).to_dict())
print("Top 5 states:", state.head(5).round(0).to_dict())
print("Top 5 products:", prod.S.nlargest(5).round(0).to_dict(), "share %:", round(prod.S.nlargest(5).sum() / prod.S.sum() * 100, 1))
print("Lowest margin products:", prod.M.nsmallest(3).round(1).to_dict(), "| highest:", prod.M.nlargest(3).round(1).to_dict())
print("\nDiscount table:\n", disc.round(2))
print("Orders with discount >= 15%:", int((df.Discount_Percent >= 15).sum()), round((df.Discount_Percent >= 15).mean() * 100, 1), "%")
print("Corr(discount, quantity):", round(df.Discount_Percent.corr(df.Quantity), 3))
print("\nLoss rate by payment mode:\n", (pay["mean"] * 100).round(1).to_dict())
for col in ["Payment_Mode", "Category", "Region"]:
    p = stats.chi2_contingency(pd.crosstab(df[col], df.Lost))[1]
    print(f"Chi-square p-value, loss rate vs {col}: {p:.3f}  ({'significant' if p < .05 else 'NOT significant at 5%'})")

# ---------------- Charts ----------------
fig, ax = plt.subplots(figsize=(10, 4.5))
x = monthly.index.to_timestamp()
ax.plot(x, lakh(monthly.Sales), marker="o", color=NAVY, label="Net sales")
ax.plot(x, lakh(monthly.Profit), marker="o", color=GREEN, label="Net profit")
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y")); ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, 2)))
ax.set_title("Monthly Net Sales & Profit (Rs lakhs)"); ax.legend(frameon=False); ax.grid(axis="y", alpha=.25)
save("1_monthly_trend")

for s, name, title, colr in [(cat.S, "2_category", "Net Sales by Category", NAVY), (reg.S, "3_region", "Net Sales by Region", GREEN)]:
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(s.index, lakh(s), color=colr)
    ax.bar_label(bars, labels=[f"{lakh(v):.2f} L ({v / s.sum() * 100:.0f}%)" for v in s], padding=4)
    ax.set_title(f"{title} (Rs lakhs)"); ax.set_xlim(0, lakh(s.max()) * 1.25)
    save(name)

t10 = prod.S.nlargest(10).sort_values()
fig, ax = plt.subplots(figsize=(8, 4.8))
bars = ax.barh(t10.index, t10 / 1e3, color=PURPLE); ax.bar_label(bars, fmt="%.0f", padding=3)
ax.set_title("Top 10 Products by Net Sales (Rs thousands)"); ax.set_xlim(0, t10.max() / 1e3 * 1.12)
save("4_top_products")

fig, ax = plt.subplots(figsize=(8, 4.8))
t5 = prod.S.nlargest(10).index
m = prod.loc[t5].M.sort_values()
ax.barh(m.index, m, color=[RED if v < 37 else AMBER for v in m]); ax.axvline(prod.P.sum() / prod.S.sum() * 100, color="k", ls="--", lw=1)
ax.set_title("Profit Margin % of the Top 10 Sellers (dashed = overall margin)"); ax.set_xlabel("Margin %")
save("5_top_seller_margin")

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
a1.bar(disc.index.astype(str) + "%", disc.M, color=[NAVY, NAVY, NAVY, AMBER, RED, RED]); a1.set_title("Profit Margin % by Discount"); a1.set_ylim(0, 50)
for i, v in enumerate(disc.M): a1.text(i, v + 1, f"{v:.1f}", ha="center")
a2.bar(disc.index.astype(str) + "%", disc.Q, color="#94A3B8"); a2.set_title("Avg Units per Order by Discount"); a2.set_ylim(0, 3)
for i, v in enumerate(disc.Q): a2.text(i, v + .05, f"{v:.2f}", ha="center")
save("6_discount_margin_vs_quantity")

fig, ax = plt.subplots(figsize=(8, 4))
pp = (pay["mean"] * 100).sort_values()
bars = ax.barh(pp.index, pp, color="#64748B"); ax.bar_label(bars, fmt="%.1f%%", padding=3)
ax.set_title("Returned + Cancelled Rate by Payment Mode (% of orders)"); ax.set_xlim(0, 14)
save("7_loss_rate_payment")

st = state.head(10).sort_values()
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(st.index, lakh(st), color=GREEN); ax.bar_label(bars, fmt="%.2f", padding=3)
ax.set_title("Top 10 States by Net Sales (Rs lakhs)"); ax.set_xlim(0, lakh(st.max()) * 1.15)
save("8_top_states")
print("\nCharts saved to", CH)
