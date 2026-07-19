import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime
from collections import defaultdict
from dateutil.relativedelta import relativedelta

month = int(sys.argv[1]) if len(sys.argv) > 1 else 1

csv_file  = "D:/wamp64/www/semsixpro/temp/files/sales/sales_all.csv"
chart_file = f"D:/wamp64/www/semsixpro/temp/files/charts/customer_charts/customer_{month}_month.png"

today = datetime.today()

# -------- build period labels --------
if month == 1:
    periods = ["Week1", "Week2", "Week3", "Week4"]
else:
    current = today.replace(day=1)
    periods = []
    for i in range(month):
        m = current.month - (month - 1 - i)
        y = current.year
        if m <= 0:
            m += 12
            y -= 1
        periods.append(f"{y}-{m:02d}")

# -------- read csv --------
customer_totals = defaultdict(float)
customer_qty    = defaultdict(float)
period_customer = defaultdict(lambda: defaultdict(float))

with open(csv_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        d = datetime.strptime(row["Sales Date"], "%Y-%m-%d")
        if d > today:
            continue

        if month == 1:
            if d.month != today.month or d.year != today.year:
                continue
            if d.day <= 7:    period = "Week1"
            elif d.day <= 14: period = "Week2"
            elif d.day <= 21: period = "Week3"
            else:             period = "Week4"
        else:
            if d < today - relativedelta(months=month):
                continue
            period = d.strftime("%Y-%m")

        name   = row.get("Customer Name", "Unknown").strip() or "Unknown"
        amount = float(row["Final Amount"])
        qty    = float(row.get("Quantity", 0))

        customer_totals[name] += amount
        customer_qty[name]    += qty
        period_customer[period][name] += amount

# -------- top 10 customers --------
top10     = sorted(customer_totals.items(), key=lambda x: x[1], reverse=True)[:10]
customers = [c[0] for c in top10]

purple_shades = [
    "#C4B5FD", "#A78BFA", "#8B5CF6", "#7C3AED",
    "#6D28D9", "#5B21B6", "#4C1D95", "#3B0F85",
    "#2E0B6E", "#1E0550"
]
colors = purple_shades[:len(customers)]

# =========================
# CREATE CHART
# =========================
fig, ax = plt.subplots(figsize=(12, 7), facecolor="#F8FAFC")
ax.set_facecolor("#FFFFFF")

y       = np.arange(len(periods))   # ← y axis now holds periods
lefts   = np.zeros(len(periods))    # ← left offset instead of bottom

for idx, customer in enumerate(customers):
    vals = [period_customer[p].get(customer, 0) for p in periods]
    ax.barh(y, vals, left=lefts, color=colors[idx], label=customer)  # ← barh + left
    lefts += np.array(vals)

# total label at end of each bar
for i, total in enumerate(lefts):
    if total > 0:
        ax.text(total, i, f" ₹{total:,.0f}", va='center', fontsize=8, fontweight='bold')  # ← va center

ax.set_yticks(y)
ax.set_yticklabels(periods, fontsize=10)          # ← periods on Y axis
ax.set_ylabel("Period", fontsize=11)
ax.set_xlabel("Sales Amount", fontsize=11)        # ← amount on X axis
ax.set_title("Top Customers by Sales (Period Wise)", fontsize=14, weight="bold")
ax.grid(axis='x', linestyle='--', alpha=0.5)      # ← grid on x axis now
for spine in ax.spines.values():
    spine.set_visible(False)

# -------- legend --------
legend_handles = []
for idx, customer in enumerate(customers):
    total = customer_totals[customer]
    qty   = int(customer_qty[customer])
    label = f"{customer}   ₹{total:,.0f}   (Qty: {qty})"
    legend_handles.append(mpatches.Patch(color=colors[idx], label=label))

ax.legend(
    handles=legend_handles,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=2,
    fontsize=9,
    frameon=True,
    edgecolor="#E5E7EB",
    fancybox=True
)

plt.tight_layout()
plt.savefig(chart_file, bbox_inches='tight')
plt.close()
