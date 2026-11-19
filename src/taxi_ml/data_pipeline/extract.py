
from pathlib import Path
import requests

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
RAW_DIR = Path("data/raw")

MONTHS = ["2025-01"]


def download_data():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for month in MONTHS:
        filename = f"yellow_tripdata_{month}.parquet"
        url = f"{BASE_URL}/{filename}"
        destination = RAW_DIR / filename

        if destination.exists():
            print(f"Already downloaded: {filename}")
            continue

        response = requests.get(url, timeout=120)
        response.raise_for_status()

        destination.write_bytes(response.content)
        print(f"Downloaded: {filename}")


if __name__ == "__main__":
    download_data()
