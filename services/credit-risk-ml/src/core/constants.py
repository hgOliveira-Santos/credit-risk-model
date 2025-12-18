from typing import List, Dict

# ==============================================================================
# COLUMN DEFINITIONS
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

# ==============================================================================
# FEATURE SELECTION FOR MODELLING
# ==============================================================================

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

# ==============================================================================
# BUSINESS RULES (Risk Thresholds)
# ==============================================================================

# If the risk probability is below 0.35, it is considered safe.
RISK_THRESHOLD_LOW = 0.35

# If the risk probability is above 0.75, it is considered dangerous.
RISK_THRESHOLD_HIGH = 0.75

# Between these values, the risk is "Medium".

# ==============================================================================
# HYPERPARAMETERS
# ==============================================================================

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

