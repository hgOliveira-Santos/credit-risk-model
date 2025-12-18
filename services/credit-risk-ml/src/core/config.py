import json
from pathlib import Path
from typing import Dict, Any
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

from src.core.paths import get_project_paths

from src.core.constants import (
    COLUMN_NAMES,
    NUMERIC_COLUMNS,
    CATEGORICAL_COLUMNS,
    TARGET_COLUMN,
    MODEL_NUMERIC_COLUMNS,
    MODEL_CATEGORICAL_COLUMNS,
    LOG_TRANSFORMER_FEATURES,
    MODEL_FEATURES,
    RISK_THRESHOLD_LOW,
    RISK_THRESHOLD_HIGH,
    RANDOM_STATE,
    TEST_SIZE,
    MODEL_PARAMS,
)


class Settings(BaseSettings):
    """
    Main configuration class for the Credit Risk ML Service.

    Loads environment-dependent settings and provides access to
    project paths and auxiliary mapping files.
    Utilizes Pydantic for robust settings management.
    """

    # --------------------------------------------------------------------------
    # Project metadata and environment-configurable fields
    # --------------------------------------------------------------------------
    PROJECT_NAME: str = "Credit Risk ML Service"

    DATA_SOURCE_URL: str = Field(
        default="http://dummy.url/for/dev",
        env="DATA_SOURCE_URL"
    )

    GERMAN_DATA_FILENAME: str = "german.data"
    CREDIT_DATA_FILENAME: str = "credit_data.data"

    # Configuration: support loading from .env and ignore unknown fields
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --------------------------------------------------------------------------
    # Path accessors
    # --------------------------------------------------------------------------
    
    def __init__(self, **kwargs):
        """Initialize Settings and create Paths instance."""
        super().__init__(**kwargs)
        self._paths = get_project_paths()

    @property
    def root_dir(self) -> Path:
        """Returns the absolute path to the project root directory."""
        return self._paths.root_dir

    @property
    def data_dir(self) -> Path:
        """Path to the top-level data directory."""
        return self._paths.data_dir

    @property
    def raw_data_dir(self) -> Path:
        """Path to the directory containing original/raw datasets."""
        return self._paths.raw_data_dir

    @property
    def processed_data_dir(self) -> Path:
        """Path to the directory containing preprocessed datasets."""
        return self._paths.processed_data_dir

    @property
    def models_prod_dir(self) -> Path:
        """Path to the directory containing production-ready models."""
        return self._paths.models_prod_dir

    @property
    def models_staging_dir(self) -> Path:
        """Path to the directory for models in staging/experimentation."""
        return self._paths.models_staging_dir

    @property
    def assets_dir(self) -> Path:
        """Path to the assets directory (e.g., for mappings, configs, vocab)."""
        return self._paths.assets_dir

    @property
    def mappings(self) -> Dict[str, Any]:
        """
        Loads feature value mappings from JSON file located in the assets directory.
        Returns an empty dictionary if the JSON file does not exist or cannot be read.
        """
        mappings_file = self.assets_dir / "mappings.json"

        if not mappings_file.exists():
            logger.warning(f"[CONFIG] File {mappings_file} not found. Returning empty dict.")
            return {}

        try:
            with open(mappings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"[CONFIG] Failed to read {mappings_file}: {e}")
            return {}


# ==============================================================================
# GLOBAL SETTINGS INSTANCE
# ==============================================================================
# Instantiated configuration object for importing and referencing project-wide settings.
settings = Settings()
