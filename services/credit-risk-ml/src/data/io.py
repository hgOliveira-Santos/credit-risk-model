import pandas as pd
import joblib
from pathlib import Path
from typing import Any


def load_csv_data(filepath: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(filepath, encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found at: {filepath}")


def save_model(model: Any, filepath: Path) -> None:
    """Save a model object to the specified filepath using joblib."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath)
    print(f"Model saved at: {filepath}")


def load_model(filepath: Path) -> Any:
    """Load a model object from the specified filepath."""
    if not filepath.exists():
        raise FileNotFoundError(f"Model not found at: {filepath}")
    return joblib.load(filepath)
