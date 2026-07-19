import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

month = int(sys.argv[1]) if len(sys.argv) > 1 else 1

sales_csv    = "D:/wamp64/www/semsixpro/temp/files/sales/sales_all.csv"
purchase_csv = "D:/wamp64/www/semsixpro/temp/files/purchase/purchase_all.csv"
expense_csv  = "D:/wamp64/www/semsixpro/temp/files/expenses/expenses_all.csv"

chart_file = f"D:/wamp64/www/semsixpro/temp/files/charts/profit_loss/profit_loss_{month}_month.png"

today = datetime.today()

# ---------- helper function ----------
def read_csv_sum(file, date_field, amount_field, fmt):
    data = defaultdict(float)

    with open(file) as f:
        for r in csv.DictReader(f):
            d = datetime.strptime(r[date_field], "%Y-%m-%d")

            if month == 1:
                if start_date <= d <= today:
                    key = d.strftime(fmt)
                    data[key] += float(r[amount_field])
            else:
                key = d.strftime("%Y-%m")
                if key in months:
                    data[key] += float(r[amount_field])

    return data


# ==================================================
# DAILY (1 MONTH)
# ==================================================
if month == 1:

    start_date = today - timedelta(days=29)

    sales    = read_csv_sum(sales_csv, "Sales Date", "Final Amount", "%d-%m")
    purchase = read_csv_sum(purchase_csv, "Date", "Amount", "%d-%m")
    expense  = read_csv_sum(expense_csv, "Expense Date", "Amount", "%d-%m")

    keys = sorted(set(sales) | set(purchase) | set(expense),
                  key=lambda x: datetime.strptime(x, "%d-%m"))

# ==================================================
# MONTHLY (4 / 6 / 12)
# ==================================================
else:

    current = today.replace(day=1)
    months = []

    for i in range(month):
        m = current.month - i
        y = current.year
        if m <= 0:
            m += 12
            y -= 1
        months.append(f"{y}-{m:02d}")

    months.reverse()

    sales    = read_csv_sum(sales_csv, "Sales Date", "Final Amount", "%Y-%m")
    purchase = read_csv_sum(purchase_csv, "Date", "Amount", "%Y-%m")
    expense  = read_csv_sum(expense_csv, "Expense Date", "Amount", "%Y-%m")

    keys = months


# ---------- calculate profit ----------
labels = []
values = []

for k in keys:
    profit = sales[k] - purchase[k] - expense[k]
    labels.append(k)
    values.append(profit)

# ---------- chart ----------
x = np.arange(len(labels))

plt.figure(figsize=(11,5))

# theme colors
line_color = "#7C3AED"
profit_fill = "#A78BFA"
loss_fill = "#FCA5A5"

# zero line
plt.axhline(0, linestyle="--", color="#9CA3AF", linewidth=1)

# main line
plt.plot(
    x,
    values,
    marker="o",
    linewidth=2.5,
    color=line_color
)

# fill areas
plt.fill_between(
    x, values, 0,
    where=[v >= 0 for v in values],
    color=profit_fill,
    alpha=0.35
)

plt.fill_between(
    x, values, 0,
    where=[v < 0 for v in values],
    color=loss_fill,
    alpha=0.35
)

# axis labels
plt.xticks(x, labels, rotation=35, ha="right")

plt.title(
f"Profit / Loss Trend – Last {month} Month{'s' if month>1 else ''}",
fontsize=13,
fontweight="bold"
)

plt.xlabel("Date" if month==1 else "Month")
plt.ylabel("Amount (₹)")

# value labels
for i,v in enumerate(values):

    offset = max(values)*0.02 if values else 100

    if v >= 0:
        plt.text(i, v+offset, f"₹{v:,.0f}", ha="center", fontsize=9)
    else:
        plt.text(i, v-offset, f"₹{v:,.0f}", ha="center", fontsize=9)

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(chart_file)
plt.close()
