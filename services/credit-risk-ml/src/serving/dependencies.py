from functools import lru_cache
from typing import Any
from loguru import logger

from src.core.config import settings
from src.data.io import load_model


@lru_cache()
def get_model() -> Any: 
    model_path = settings.models_prod_dir / "model.pkl"
    logger.info(f"[API] Loading model from: {model_path} ...")

    try:
        model = load_model(model_path)
        logger.info("[API] Model successfully loaded.")
        return model
    except FileNotFoundError:
        logger.critical("[CRITICAL] Model not found.")
        raise