import csv
import json
import requests

CSV_URL = "https://storage.googleapis.com/play_public/supported_devices.csv"
OUTPUT_FILE = "devices.json"

def fetch_and_convert():
    resp = requests.get(CSV_URL)
    resp.raise_for_status()
    text = resp.text

    reader = csv.DictReader(text.splitlines())
    mapping = {}
    for row in reader:
        device_code = row.get("Device")
        marketing_name = row.get("Marketing Name")
        retail_brand = row.get("Retail Branding")  # optional
        if device_code and marketing_name:
            # Store as nested JSON: includes brand and name
            mapping[device_code.strip()] = {
                "brand": retail_brand.strip() if retail_brand else "",
                "name": marketing_name.strip()
            }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(mapping)} devices to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_convert()