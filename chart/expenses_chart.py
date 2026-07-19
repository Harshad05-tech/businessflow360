import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict

month = int(sys.argv[1]) if len(sys.argv) > 1 else 1

csv_file = "D:/wamp64/www/semsixpro/temp/files/expenses/expenses_all.csv"
chart_file = f"D:/wamp64/www/semsixpro/temp/files/charts/expenses_charts/expenses_{month}_month.png"

today = datetime.today()

# -------- last N months --------
required_months = []
for i in range(month):
    m = today.month - i
    y = today.year
    if m <= 0:
        m += 12
        y -= 1
    required_months.append(f"{y}-{m:02d}")

# -------- read data --------
expense_data = defaultdict(float)

with open(csv_file) as f:
    reader = csv.DictReader(f)

    for row in reader:
        d = datetime.strptime(row["Expense Date"], "%Y-%m-%d")

        if d > today:
            continue

        if d.strftime("%Y-%m") in required_months:
            name = row["Expense Name"].strip()
            expense_data[name] += float(row["Amount"])

# -------- no data --------
if not expense_data:
    plt.figure(figsize=(10,5))
    plt.text(0.5,0.5,"No Data Available",ha="center",va="center")
    plt.xticks([])
    plt.yticks([])
    plt.savefig(chart_file)
    plt.close()
    exit()

# -------- sort data --------
data = sorted(expense_data.items(), key=lambda x:x[1], reverse=True)

labels = [i[0] for i in data]
values = [i[1] for i in data]

# shorten long names
labels = [l[:13]+"…" if len(l)>13 else l for l in labels]

x = np.arange(len(labels))

# -------- chart --------
plt.figure(figsize=(10,5))
plt.bar(x, values, color="#7C3AED")

plt.xticks(x, labels, rotation=35, ha="right")
plt.title(f"Expenses – Last {month} Month{'s' if month>1 else ''}")
plt.xlabel("Expense Name")
plt.ylabel("Amount")

plt.grid(axis="y", linestyle="--", alpha=0.5)

# value labels
for i,v in enumerate(values):
    plt.text(i, v, f"₹{v:,.0f}", ha="center", va="bottom")

plt.tight_layout()
plt.savefig(chart_file)
plt.close()