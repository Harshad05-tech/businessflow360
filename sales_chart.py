import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict

month = int(sys.argv[1]) if len(sys.argv) > 1 else 1

csv_file = "D:/wamp64/www/semsixpro/temp/files/sales/sales_all.csv"
chart_file = f"D:/wamp64/www/semsixpro/temp/files/charts/sales_charts/sales_{month}_month.png"

today = datetime.today()

# =========================
# 1 MONTH → WEEK WISE
# =========================
if month == 1:

    week_sales = defaultdict(float)

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = datetime.strptime(row["Sales Date"], "%Y-%m-%d")

            if d.month == today.month and d.year == today.year and d <= today:

                if d.day <= 7:
                    week = "Week1"
                elif d.day <= 14:
                    week = "Week2"
                elif d.day <= 21:
                    week = "Week3"
                else:
                    week = "Week4"

                week_sales[week] += float(row["Final Amount"])

    labels = ["Week1", "Week2", "Week3", "Week4"]
    values = [week_sales.get(w,0) for w in labels]

# =========================
# MULTIPLE MONTH → MONTH WISE
# =========================
else:

    monthly_sales = defaultdict(float)

    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = datetime.strptime(row["Sales Date"], "%Y-%m-%d")

            if d <= today:
                key = d.strftime("%Y-%m")
                monthly_sales[key] += float(row["Final Amount"])

    current = today.replace(day=1)

    labels = []
    for i in range(month):
        m = current.month - (month - 1 - i)
        y = current.year

        if m <= 0:
            m += 12
            y -= 1

        labels.append(f"{y}-{m:02d}")

    values = [monthly_sales.get(m,0) for m in labels]


# =========================
# CREATE CHART
# =========================

x = np.arange(len(labels))

plt.figure(figsize=(10,5), facecolor="#F8FAFC")
ax = plt.gca()
ax.set_facecolor("#FFFFFF")

bars = plt.bar(x, values, color="#7C3AED")

plt.xticks(x, labels)
plt.title("Sales Chart", fontsize=14, weight="bold")
plt.xlabel("Time")
plt.ylabel("Sales Amount")

plt.grid(axis='y', linestyle='--', alpha=0.5)

for i, v in enumerate(values):
    if v > 0:
        plt.text(i, v, f"₹{v:,.0f}", ha='center', va='bottom')

for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig(chart_file)
plt.close()
