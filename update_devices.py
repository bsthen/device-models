import csv
import json
import requests

CSV_URL = "https://storage.googleapis.com/play_public/supported_devices.csv"
OUTPUT_FILE = "devices.json"

def fetch_and_convert():
    resp = requests.get(CSV_URL)
    resp.raise_for_status()
    text = resp.text

    # Read CSV
    reader = csv.reader(text.splitlines())

    # Skip header
    next(reader)

    mapping = {}
    for row in reader:
        if len(row) < 4:
            continue

        retail_brand = row[0].strip()      # Column 0
        marketing_name = row[1].strip()    # Column 1
        device_code = row[3].strip()       # Column 3

        if not device_code or not marketing_name:
            continue

        mapping[device_code] = {
            "brand": retail_brand,
            "name": marketing_name
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(mapping)} devices to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_convert()
