import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from collections import defaultdict

month = int(sys.argv[1]) if len(sys.argv) > 1 else 1

csv_file = "D:/wamp64/www/semsixpro/temp/files/sales/sales_all.csv"
chart_file = f"D:/wamp64/www/semsixpro/temp/files/charts/sales_pie/item_pie_{month}_month.png"

today = datetime.today()

# ---------- start date ----------
y = today.year
m = today.month - (month - 1)

if m <= 0:
    y -= (abs(m) // 12) + 1
    m = 12 - (abs(m) % 12)

start_date = datetime(y, m, 1)

# ---------- data ----------
item_data = defaultdict(lambda: {"qty":0,"value":0})

with open(csv_file) as f:
    reader = csv.DictReader(f)

    for row in reader:
        d = datetime.strptime(row["Sales Date"], "%Y-%m-%d")

        if d > today:
            continue

        if start_date <= d <= today:
            item = row["Item"]
            qty  = float(row["Quantity"])
            amt  = float(row["Final Amount"])

            item_data[item]["qty"] += qty
            item_data[item]["value"] += amt


# ---------- sort ----------
data = sorted(item_data.items(), key=lambda x:x[1]["value"], reverse=True)

labels = []
values = []
qtys   = []

for item, d in data:
    if d["value"] > 0:
        labels.append(item)
        values.append(d["value"])
        qtys.append(d["qty"])


# ---------- no data ----------
if not values:
    plt.figure(figsize=(8,8))
    plt.text(0.5,0.5,"No Data Available",ha="center",va="center",fontsize=14)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(chart_file)
    plt.close()
    exit()


# ---------- colors ----------
colors = [
"#5B21B6","#7C3AED","#8B5CF6","#A78BFA",
"#C4B5FD","#DDD6FE","#EDE9FE","#6D28D9"
]

colors = [colors[i % len(colors)] for i in range(len(values))]

total = sum(values)

# ---------- pie ----------
fig, ax = plt.subplots(figsize=(9,8))

def autopct_format(pct):
    total_val = sum(values)
    val = pct * total_val / 100

    for label, v in zip(labels, values):
        if abs(v - val) < 1:
            return f"{label}\n{pct:.1f}%"
    return f"{pct:.1f}%"

wedges, _, autotexts = ax.pie(
    values,
    colors=colors,
    autopct=autopct_format,
    startangle=140,
    pctdistance=0.75,
    wedgeprops=dict(width=0.45)
)

# improve text readability
for t in autotexts:
    t.set_fontsize(13)
    t.set_color("white")
    t.set_weight("bold")

# ---------- center text ----------
ax.text(0,0.1,"Total Sales",ha="center",fontsize=12,color="#6B7280")
ax.text(0,-0.1,f"₹{total:,.0f}",ha="center",fontsize=16,weight="bold")

# ---------- legend ----------
legend_labels = [
f"{l}   ₹{v:,.0f}  (Qty: {int(q)})"
for l,v,q in zip(labels,values,qtys)
]

patches = [
mpatches.Patch(color=colors[i],label=legend_labels[i])
for i in range(len(labels))
]

ax.legend(
handles=patches,
loc="lower center",
bbox_to_anchor=(0.5,-0.20),
ncol=2,
fontsize=14,     # bigger legend text
frameon=True
)

# ---------- title ----------
ax.set_title(
f"Item Wise Sales – Last {month} Month{'s' if month>1 else ''}",
fontsize=14,
weight="bold"
)

plt.tight_layout()
plt.savefig(chart_file,bbox_inches="tight")
plt.close()