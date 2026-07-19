import requests

url = "https://businessflow360.infinityfree.me/files/sales/sales_all.csv"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=30)

print(response.status_code)

with open("sales_all.csv", "wb") as f:
    f.write(response.content)
