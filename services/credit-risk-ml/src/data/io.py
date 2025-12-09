import pandas as pd

import joblib
from pathlib import Path
from typing import Any
from src.core.config import COLUMN_NAMES


def load_raw_data(filepath: Path) -> pd.DataFrame:
    """
    Loads the original dataset (german.data).

    The raw file characteristics:
    - Space-separated (sep=" ")
    - No header row (header=None)
    - UTF-8 encoding

    Column names are applied as defined in configuration.
    """
    try:
        df = pd.read_csv(
            filepath, sep=" ", header=None, names=COLUMN_NAMES, encoding="utf-8"
        )
        print(f"[IO] Data loaded. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found at: {filepath}")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {e}")


def save_model(model: Any, filepath: Path) -> None:
    """
    Saves the trained model (pipeline) using joblib.
    """
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, filepath)
        print(f"[IO] Model saved at: {filepath}")
    except Exception as e:
        print(f"[IO] Error saving model: {e}")
        raise e


def load_model(filepath: Path) -> Any:
    """
    Loads a trained model from disk.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Model not found at: {filepath}")

    try:
        return joblib.load(filepath)
    except Exception as e:
        print(f"[IO] Error loading model: {e}")
        raise e
