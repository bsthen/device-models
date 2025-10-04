# Device Models

This repository provides a **mapping of device codes to marketing names** for Android and other smartphones. The data is sourced from the publicly available Google Play supported devices list and updated automatically via GitHub Actions.

---

## Features

- **Device code → Marketing name mapping**  
- Includes the **brand** of each device.  
- Auto-updated **weekly** from Google’s CSV.  
- JSON format for easy integration in apps, APIs, or scripts.  

---

## Example JSON Format

```json
{
  "SM-G965F": {
    "brand": "Samsung",
    "name": "Samsung Galaxy S9+"
  },
  "SM-G960F": {
    "brand": "Samsung",
    "name": "Samsung Galaxy S9"
  }
}
```

# Usage

## Python Example

```bash
import requests

DEVICES_URL = "https://raw.githubusercontent.com/bsthen/device-models/main/devices.json"

resp = requests.get(DEVICES_URL)
device_map = resp.json()

device_code = "SM-G965F"
device = device_map.get(device_code)

if device:
    print(f"{device_code} → {device['brand']} {device['name']}")
else:
    print("Device not found")
```

## FastAPI Example

```bash
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()
DEVICES_URL = "https://raw.githubusercontent.com/bsthen/device-models/main/devices.json"
device_map = requests.get(DEVICES_URL).json()

@app.get("/device")
def get_device(code: str):
    device = device_map.get(code.upper())
    if device:
        return {"code": code, "brand": device.get("brand"), "name": device.get("name")}
    raise HTTPException(status_code=404, detail="Device not found")

```

# GitHub Actions

This repository uses GitHub Actions to automatically fetch the latest supported devices CSV from Google, convert it to JSON, and commit updates weekly.

# License

This repository is licensed under the [Apache License 2.0](https://github.com/bsthen/device-models?tab=Apache-2.0-1-ov-file).

# Notes

- The dataset is based on Google’s publicly available supported devices list:
[https://storage.googleapis.com/play_public/supported_devices.html](https://storage.googleapis.com/play_public/supported_devices.html)

- Device codes are usually manufacturer/model identifiers (e.g., SM-G965F for Samsung Galaxy S9+).