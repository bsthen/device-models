import csv
import json
import requests
import unicodedata

# URL of Google Play supported devices CSV
CSV_URL = "https://storage.googleapis.com/play_public/supported_devices.csv"
OUTPUT_FILE = "devices.json"

def fetch_and_convert():
    resp = requests.get(CSV_URL)
    resp.raise_for_status()
    text = resp.text

    # Read CSV with DictReader
    reader = csv.DictReader(text.splitlines())

    # Strip headers in case of trailing spaces
    reader.fieldnames = [h.strip() for h in reader.fieldnames]

    mapping = {}
    for row in reader:
        # Normalize strings to remove hidden characters
        device_code = unicodedata.normalize("NFKC", row.get("Model", "").strip())
        marketing_name = unicodedata.normalize("NFKC", row.get("Marketing Name", "").strip())
        retail_brand = unicodedata.normalize("NFKC", row.get("Retail Branding", "").strip())

        # Skip rows with empty device code or marketing name
        if not device_code or not marketing_name:
            continue

        # Store in mapping
        mapping[device_code] = {
            "brand": retail_brand,
            "name": marketing_name
        }

    # Save to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"✅ Converted {len(mapping)} devices to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_and_convert()
