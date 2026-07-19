import requests
import subprocess
import os
from ftplib import FTP

# ===========================
# Download CSV
# ===========================

csv_url = "https://businessflow360.infinityfree.me/files/sales/sales_all.csv"

try:
    print("Downloading CSV...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        csv_url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    with open("sales_all.csv", "wb") as file:
        file.write(response.content)

    print("CSV downloaded successfully.")

except Exception as e:
    print("CSV Download Error")
    print(e)
    exit(1)


# ===========================
# Generate Chart
# ===========================

try:

    print("Generating Chart...")

    subprocess.run(
        ["python", "sales_chart.py"],
        check=True
    )

    print("Chart Generated Successfully.")

except Exception as e:

    print("Chart Generation Error")
    print(e)
    exit(1)


# ===========================
# Check PNG Exists
# ===========================

if not os.path.exists("sales_chart.png"):
    print("sales_chart.png not found.")
    exit(1)


# ===========================
# Upload to FTP
# ===========================

try:

    print("Connecting FTP...")

    ftp = FTP(os.environ["FTP_HOST"])

    ftp.login(
        os.environ["FTP_USER"],
        os.environ["FTP_PASS"]
    )

    ftp.cwd("/htdocs/charts/sales_chart")

    with open("sales_chart.png", "rb") as file:
        ftp.storbinary(
            "STOR sales_chart.png",
            file
        )

    ftp.quit()

    print("Chart Uploaded Successfully.")

except Exception as e:

    print("FTP Upload Error")
    print(e)
    exit(1)
