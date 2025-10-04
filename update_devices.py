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
    reader.fieldnames = [h.strip() for h in reader.fieldnames]  # clean headers

    mapping = {}
    for row in reader:
        device_code = row.get("Device", "").strip()
        marketing_name = row.get("Marketing Name", "").strip()
        retail_brand = row.get("Retail Branding", "").strip()

        # skip empty device codes
        if not device_code:
            continue

        # if device already in mapping, keep existing name if it's non-empty
        if device_code in mapping and mapping[device_code]["name"]:
            continue

        # store only if marketing name is available
        if marketing_name:
            mapping[device_code] = {
                "brand": retail_brand,
                "name": marketing_name
            }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(mapping)} devices to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_convert()
