import json
from pathlib import Path
from typing import Dict, List, Any
from pydantic import computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ==============================================================================
# 1. DOMAIN CONSTANTS
# ==============================================================================

# ------------------------------------------------------------------------------
# COLUMN_NAMES
# ------------------------------------------------------------------------------
# List of all column names in the raw dataset, ordered as per the official documentation.
COLUMN_NAMES: List[str] = [
    "checking_account_status",
    "duration_in_month",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings_account_bonds",
    "present_employment_since",
    "installment_rate_percent",
    "personal_status_and_sex",
    "other_debtors_guarantors",
    "present_residence_since",
    "property",
    "age_in_years",
    "other_installment_plans",
    "housing",
    "number_of_existing_credits",
    "job",
    "number_of_dependents",
    "telephone",
    "foreign_worker",
    "risk",
]

# ------------------------------------------------------------------------------
# NUMERIC_COLUMNS
# ------------------------------------------------------------------------------
# Columns interpreted as numerical (continuous or discrete, suitable for scaler/transformations).
NUMERIC_COLUMNS: List[str] = [
    "duration_in_month",
    "credit_amount",
    "installment_rate_percent",
    "present_residence_since",
    "age_in_years",
    "number_of_existing_credits",
    "number_of_dependents",
]

# ------------------------------------------------------------------------------
# CATEGORICAL_COLUMNS
# ------------------------------------------------------------------------------
# Columns interpreted as categorical or ordinal (suitable for encoding strategies).
CATEGORICAL_COLUMNS: List[str] = [
    "checking_account_status",
    "credit_history",
    "purpose",
    "savings_account_bonds",
    "present_employment_since",
    "personal_status_and_sex",
    "other_debtors_guarantors",
    "property",
    "other_installment_plans",
    "housing",
    "job",
    "telephone",
    "foreign_worker",
]

# ------------------------------------------------------------------------------
# TARGET_COLUMN
# ------------------------------------------------------------------------------
# The label column to predict.
TARGET_COLUMN: str = "risk"

# ------------------------------------------------------------------------------
# FEATURE SELECTION FOR MODELLING
# ------------------------------------------------------------------------------
# Model-selected numeric input features.
MODEL_NUMERIC_COLUMNS: List[str] = [
    "credit_amount",
    "duration_in_month",
    "age_in_years",
    "installment_rate_percent",
    "present_residence_since"
]

# Model-selected categorical input features.
MODEL_CATEGORICAL_COLUMNS: List[str] = [
    "checking_account_status",
    "credit_history",
    "purpose",
    "property",
    "savings_account_bonds",
    "present_employment_since",
]

# Columns to apply log transformation during preprocessing.
LOG_TRANSFORMER_FEATURES: List[str] = ["credit_amount"]

# Complete ordered feature list for the model pipeline.
MODEL_FEATURES: List[str] = MODEL_NUMERIC_COLUMNS + MODEL_CATEGORICAL_COLUMNS

# ------------------------------------------------------------------------------
# HYPERPARAMETERS
# ------------------------------------------------------------------------------
# Global random state for reproducibility.
RANDOM_STATE = 42

# Test split fraction.
TEST_SIZE = 0.2

# Default training hyperparameters (e.g., for RandomForestClassifier).
MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'random_state': RANDOM_STATE,
    'class_weight': 'balanced'
}

# ==============================================================================
# 2. CONFIGURATION CLASS
# ==============================================================================

class Settings(BaseSettings):
    """
    Main configuration class for the Credit Risk ML Service.

    Loads constants, environment-dependent settings, and directory paths.
    Utilizes Pydantic for robust settings management and supports
    dynamic resource resolution. Also provides convenient loading
    of auxiliary mapping files.
    """

    # --------------------------------------------------------------------------
    # Project metadata and environment-configurable fields
    # --------------------------------------------------------------------------
    PROJECT_NAME: str = "Credit Risk ML Service"

    # Data source endpoint (overridable by env var DATA_SOURCE_URL)
    DATA_SOURCE_URL: str = Field(
        default="http://dummy.url/for/dev",
        env="DATA_SOURCE_URL"
    )

    # Dataset file naming conventions (relative to data directories)
    GERMAN_DATA_FILENAME: str = "german.data"
    CREDIT_DATA_FILENAME: str = "credit_data.data"

    # Configuration: support loading from .env and ignore unknown fields
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --------------------------------------------------------------------------
    # Path accessors for primary data, models, and assets
    # --------------------------------------------------------------------------

    @computed_field
    def root_dir(self) -> Path:
        """
        Returns the absolute path to the project root directory.
        """
        return Path(__file__).parent.parent.parent

    @property
    def data_dir(self) -> Path:
        """
        Path to the top-level data directory.
        """
        return self.root_dir / "data"

    @property
    def raw_data_dir(self) -> Path:
        """
        Path to the directory containing original/raw datasets.
        """
        return self.data_dir / "raw"

    @property
    def processed_data_dir(self) -> Path:
        """
        Path to the directory containing preprocessed datasets.
        """
        return self.data_dir / "processed"

    @property
    def models_prod_dir(self) -> Path:
        """
        Path to the directory containing production-ready models.
        """
        return self.root_dir / "models" / "prod"

    @property
    def models_staging_dir(self) -> Path:
        """
        Path to the directory for models in staging/experimentation.
        """
        return self.root_dir / "models" / "staging"

    @property
    def assets_dir(self) -> Path:
        """
        Path to the assets directory (e.g., for mappings, configs, vocab).
        """
        return self.root_dir / "src" / "assets"

    @property
    def mappings(self) -> Dict[str, Any]:
        """
        Loads feature value mappings from JSON file located in the assets directory.
        Returns an empty dictionary if the JSON file does not exist or cannot be read.
        """
        mappings_file = self.assets_dir / "mappings.json"

        if not mappings_file.exists():
            print(f"WARNING: File {mappings_file} not found. Returning empty dict.")
            return {}

        try:
            with open(mappings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Failed to read {mappings_file}: {e}")
            return {}

# ==============================================================================
# 3. GLOBAL SETTINGS INSTANCE
# ==============================================================================
# Instantiated configuration object for importing and referencing project-wide settings.
settings = Settings()

# ------------------------------------------------------------------------------
# Suggested commit message:
# ------------------------------------------------------------------------------
# Refactor configuration module for improved readability and documentation
#
# - Reformatted the config.py file for clarity and structured visual layout.
# - Rewrote all inline and block comments in English for consistency and documentation quality.
# - Clearly segmented code sections for column definitions, feature selection, hyperparameters, and directory structure.
# - Enhanced Settings class docstrings and each property with explicit usage explanations.
# - Provided a professional style for future maintainability and onboarding.
