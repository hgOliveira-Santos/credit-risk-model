import zipfile
import requests
from io import BytesIO
from pathlib import Path
from typing import Protocol, runtime_checkable
from loguru import logger

from src.core.config import settings


@runtime_checkable
class FileDownloader(Protocol):
    """Abstract interface for file downloading."""

    def get_content(self, url: str) -> bytes: ...


class RequestsFileDownloader:
    """Downloader implementation using the requests library."""

    def __init__(self, timeout: int = 60):
        self.timeout = timeout

    def get_content(self, url: str) -> bytes:
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            # Here we could raise a domain-specific exception for further decoupling if desired
            logger.error(f"[DOWNLOADER] HTTP Request failed: {e}")
            raise e


def download_dataset(
    overwrite: bool = False, downloader: FileDownloader = None
) -> Path:
    """
    Downloads the dataset from the repository (ZIP) and extracts it.

    Args:
        overwrite: Force download even if file exists.
        downloader: dependency injection for the download strategy.
                    If None, uses default RequestsFileDownloader.
    """
    # "Default" Dependency Injection (Simplified Composition Root)
    if downloader is None:
        downloader = RequestsFileDownloader()

    output_path = settings.raw_data_dir / settings.CREDIT_DATA_FILENAME

    # 1. Cache Check
    if output_path.exists() and not overwrite:
        logger.info(f"[INGESTION] File already exists at: {output_path}")
        return output_path

    logger.info(f"[INGESTION] Downloading data from {settings.DATA_SOURCE_URL} ...")

    try:
        settings.raw_data_dir.mkdir(parents=True, exist_ok=True)

        # 2. Download
        content_bytes = downloader.get_content(settings.DATA_SOURCE_URL)
        zip_buffer = BytesIO(content_bytes)

        # 3. Extract and Save
        with zipfile.ZipFile(zip_buffer) as archive:
            if settings.GERMAN_DATA_FILENAME not in archive.namelist():
                raise FileNotFoundError(
                    f"File '{settings.GERMAN_DATA_FILENAME}' not found inside ZIP."
                )

            logger.info(f"[INGESTION] Extracting '{settings.GERMAN_DATA_FILENAME}'...")

            with archive.open(settings.GERMAN_DATA_FILENAME) as source, open(
                output_path, "wb"
            ) as target:
                target.write(source.read())

        logger.success(f"[INGESTION] Dataset successfully saved at: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"[INGESTION] Data ingestion failed: {e}")
        raise e


if __name__ == "__main__":
    download_dataset(overwrite=True)
