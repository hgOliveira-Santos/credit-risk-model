import pandas as pd

from src.config import CREDIT_DATA, PROCESSED_DATA_DIR

FILE_PATH = PROCESSED_DATA_DIR / CREDIT_DATA


def load_credit_data(file_path: str = FILE_PATH) -> pd.DataFrame:
    return pd.read_parquet(file_path)
