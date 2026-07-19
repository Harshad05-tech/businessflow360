import requests
import subprocess
import os

# CSV URL
csv_url = "https://businessflow360.infinityfree.me/files/sales/sales_all.csv"

# CSV download
response = requests.get(csv_url)

with open("sales_all.csv","wb") as file:
    file.write(response.content)

print("CSV downloaded")

# sales chart generate
subprocess.run([
    "python",
    "sales_chart.py"
])

print("Sales chart generated")
