import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict

month = int(sys.argv[1]) if len(sys.argv) > 1 else 1

csv_file = "D:/wamp64/www/semsixpro/temp/files/purchase/purchase_all.csv"

supplier_chart = f"D:/wamp64/www/semsixpro/temp/files/charts/purchase_charts/supplier_{month}_month.png"
item_chart     = f"D:/wamp64/www/semsixpro/temp/files/charts/purchase_charts/item_{month}_month.png"

today = datetime.today()

# ---------- start date ----------
if month == 1:
    start_date = today.replace(day=1)
else:
    m = today.month - (month - 1)
    y = today.year
    if m <= 0:
        m += 12
        y -= 1
    start_date = datetime(y, m, 1)

supplier_data = defaultdict(float)
item_data = defaultdict(float)

# ---------- read csv ----------
with open(csv_file) as f:
    reader = csv.DictReader(f)

    for row in reader:
        try:
            d = datetime.strptime(row["Date"], "%d-%m-%Y")
        except:
            d = datetime.strptime(row["Date"], "%Y-%m-%d")

        if d > today or d < start_date:
            continue

        supplier = row["Supplier"].strip()
        item     = row["Item"].strip()
        amount   = float(row["Amount"])

        supplier_data[supplier] += amount
        item_data[item] += amount


# ---------- function to create chart ----------
def create_chart(data, path, title, xlabel, color):

    data = sorted(data.items(), key=lambda x:x[1], reverse=True)[:10]

    if not data:
        plt.figure(figsize=(10,5))
        plt.text(0.5,0.5,"No Data Available",ha="center",va="center")
        plt.xticks([])
        plt.yticks([])
        plt.savefig(path)
        plt.close()
        return

    labels = [i[0][:13]+"…" if len(i[0])>13 else i[0] for i in data]
    values = [i[1] for i in data]

    x = np.arange(len(labels))

    plt.figure(figsize=(11,5))
    plt.bar(x, values, color=color)

    plt.xticks(x, labels, rotation=30, ha="right")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Amount")

    for i,v in enumerate(values):
        plt.text(i, v, f"₹{v:,.0f}", ha="center", va="bottom")

    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(path)
    plt.close()


period = "Current Month" if month == 1 else f"Last {month} Months"

#======================== 
def create_horizontal_chart(data, path, title, xlabel, color):

    data = sorted(data.items(), key=lambda x:x[1], reverse=True)[:10]

    if not data:
        plt.figure(figsize=(10,5))
        plt.text(0.5,0.5,"No Data Available",ha="center",va="center")
        plt.xticks([])
        plt.yticks([])
        plt.savefig(path)
        plt.close()
        return

    labels = [i[0][:20]+"…" if len(i[0])>20 else i[0] for i in data]
    values = [i[1] for i in data]

    y = np.arange(len(labels))

    plt.figure(figsize=(11,6))

    plt.barh(y, values, color=color)

    plt.yticks(y, labels)
    plt.xlabel("Amount")
    plt.title(title)

    # highest value top me
    plt.gca().invert_yaxis()

    for i,v in enumerate(values):
        plt.text(v, i, f" ₹{v:,.0f}", va="center")

    plt.grid(axis="x", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

# ---------- supplier chart ----------
create_chart(
    supplier_data,
    supplier_chart,
    f"Top Suppliers by Purchase ({period})",
    "Supplier",
    "#7C3AED"
)

# ---------- item chart ----------
create_horizontal_chart(
    item_data,
    item_chart,
    f"Top Items by Purchase ({period})",
    "Item",
    "#8B5CF6"
)