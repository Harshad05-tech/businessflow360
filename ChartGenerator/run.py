import requests
import subprocess
import os
from ftplib import FTP

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

ftp = FTP(os.environ["FTP_HOST"])

ftp.login(
    os.environ["FTP_USER"],
    os.environ["FTP_PASS"]
)

with open("sales_chart.png","rb") as file:

    ftp.storbinary(
        "STOR /htdocs/charts/sales_chart/sales_chart.png",
        file
    )

ftp.quit()

print("Chart uploaded")
