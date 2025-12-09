import json
from pathlib import Path
from typing import Dict, List, Any
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# ==============================================================================
# 1. DOMAIN CONSTANTS (Static Business Rules)
# ==============================================================================

# Rename columns according to documentation
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

# Numeric columns (continuous and discrete values)
NUMERIC_COLUMNS: List[str] = [
    "duration_in_month",
    "credit_amount",
    "installment_rate_percent",
    "present_residence_since",
    "age_in_years",
    "number_of_existing_credits",
    "number_of_dependents",
]

# Categorical columns (categorical/ordinal values)
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

TARGET_COLUMN: str = "risk"

# ==============================================================================
# 2. CONFIGURATION CLASS
# ==============================================================================


class Settings(BaseSettings):
    # Project metadata
    PROJECT_NAME: str = "Credit Risk ML Service"

    # Required URL
    DATA_SOURCE_URL: str

    # Default Filenames
    GERMAN_DATA_FILENAME: str = "german.data"
    CREDIT_DATA_FILENAME: str = "credit_data.data"

    # Configuration to automatically read the .env file
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- Dynamic Path Definitions ---

    @computed_field
    def root_dir(self) -> Path:
        return Path(__file__).parent.parent.parent

    @property
    def data_dir(self) -> Path:
        return self.root_dir / "data"

    @property
    def raw_data_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def processed_data_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def models_prod_dir(self) -> Path:
        return self.root_dir / "models" / "prod"

    @property
    def models_staging_dir(self) -> Path:
        return self.root_dir / "models" / "staging"

    @property
    def assets_dir(self) -> Path:
        return self.root_dir / "src" / "assets"

    @property
    def mappings(self) -> Dict[str, Any]:
        """
        Load JSON mappings.
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
# 3. GLOBAL INSTANCE
# ==============================================================================

settings = Settings()
