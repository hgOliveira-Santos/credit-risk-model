import requests
import zipfile
from io import BytesIO
from pathlib import Path
from loguru import logger

from src.core.config import settings


def download_dataset(overwrite: bool = False) -> Path:
    """
    Downloads the dataset from the UCI repository (ZIP), extracts the data file,
    and saves it to the raw folder defined in the configuration.

    Args:
        overwrite (bool): If True, force download even if the file already exists.

    Returns:
        Path: Absolute path to the saved file.
    """
    # Set the target path: data/raw/credit_data.data
    output_path = settings.raw_data_dir / settings.CREDIT_DATA_FILENAME

    # 1. Cache Check: If path exists, skip download unless overwrite is True
    if output_path.exists() and not overwrite:
        logger.info(f"[INGESTION] File already exists at: {output_path}")
        return output_path

    logger.info(f"[INGESTION] Downloading data from {settings.DATA_SOURCE_URL} ...")

    try:
        # Ensure the data/raw directory exists
        settings.raw_data_dir.mkdir(parents=True, exist_ok=True)

        # 2. Download ZIP to memory
        response = requests.get(settings.DATA_SOURCE_URL, timeout=60)
        response.raise_for_status()
        zip_buffer = BytesIO(response.content)

        # 3. Extract and Save the data file
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
