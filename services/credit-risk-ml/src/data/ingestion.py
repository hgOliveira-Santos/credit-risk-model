import zipfile
import requests
from io import BytesIO

def download_dataset(url: str, csv_filename: str) -> BytesIO:
    """
    Downloads a ZIP file from a given URL and returns the specified CSV file in memory (BytesIO).
    """
    print(f"[EXTRACT] Downloading from {url} ...")
    try:
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()
        zip_bytes = BytesIO(response.content)
        with zipfile.ZipFile(zip_bytes) as archive:
            with archive.open(csv_filename) as csvfile:
                csv_buffer = BytesIO(csvfile.read())
        print(f"[OK] CSV '{csv_filename}' loaded into memory.")
        return csv_buffer
    except Exception as e:
        print(f"[ERROR] Failed to download or extract: {e}")
        raise e
