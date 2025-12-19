from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

# -----------------------------------------------------------------------------
# 1. Enums
# -----------------------------------------------------------------------------

class CheckingAccountStatus(str, Enum):
    NO_ACCOUNT = "A14"
    NEGATIVE_BALANCE = "A11"
    LOW_BALANCE = "A12"
    MODERATE_BALANCE = "A13"

class CreditHistory(str, Enum):
    NO_CREDITS = "A30"
    ALL_PAID_DULY = "A31"
    EXISTING_PAID_DULY = "A32"
    DELAY_IN_PAST = "A33"
    CRITICAL_ACCOUNT = "A34"

class Purpose(str, Enum):
    CAR_NEW = "A40"
    CAR_USED = "A41"
    FURNITURE_EQUIPMENT = "A42"
    RADIO_TV = "A43"
    DOMESTIC_APPLIANCES = "A44"
    REPAIRS = "A45"
    EDUCATION = "A46"
    RETRAINING = "A48"
    BUSINESS = "A49"
    OTHERS = "A410"

class SavingsAccountBonds(str, Enum):
    VERY_LOW = "A61"
    LOW = "A62"
    MODERATE = "A63"
    HIGH = "A64"
    UNKNOWN_NONE = "A65"

class EmploymentDuration(str, Enum):
    UNEMPLOYED = "A71"
    LESS_THAN_1YR = "A72"
    ONE_TO_FOUR_YRS = "A73"
    FOUR_TO_SEVEN_YRS = "A74"
    MORE_THAN_7YRS = "A75"

class PropertyType(str, Enum):
    REAL_ESTATE = "A121"
    LIFE_INSURANCE_SAVINGS = "A122"
    CAR = "A123"
    NO_PROPERTY_UNKNOWN = "A124"

# -----------------------------------------------------------------------------
# 2. Input Schema
# -----------------------------------------------------------------------------

class PredictionInput(BaseModel):
    # --- Numerical Features ---
    credit_amount: float = Field(..., gt=0, description="Credit amount applied for")
    duration_in_month: int = Field(..., gt=0, description="Duration of the credit in months")
    age_in_years: int = Field(..., ge=18, le=120, description="Age of the applicant in years")
    installment_rate_percent: int = Field(..., ge=1, le=4, description="Installment rate percent")
    present_residence_since: int = Field(..., ge=1, description="Years at current residence")

    # --- Categorical Features ---
    checking_account_status: CheckingAccountStatus = Field(..., description="Status of checking account")
    credit_history: CreditHistory = Field(..., description="Credit history status")
    purpose: Purpose = Field(..., description="Purpose of the loan")
    savings_account_bonds: SavingsAccountBonds = Field(..., description="Savings account status")
    present_employment_since: EmploymentDuration = Field(..., description="Employment duration")
    property_type: PropertyType = Field(
        ...,
        alias="property",
        description="Property ownership status"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "credit_amount": 3000.0,
                "duration_in_month": 24,
                "age_in_years": 35,
                "installment_rate_percent": 3,
                "present_residence_since": 2,
                "checking_account_statárus": "A11",
                "credit_history": "A32",
                "purpose": "A40",
                "property": "A121",
                "savings_account_bonds": "A61",
                "present_employment_since": "A73"
            }
        }
    )

# -----------------------------------------------------------------------------
# 3. Output Schema
# -----------------------------------------------------------------------------

class PredictionOutput(BaseModel):
    risk: int = Field(..., description="Predicted risk class (0=Good, 1=Bad)")
    probability: float = Field(..., description="Probability of Bad Risk")
    class_label: str = Field(..., description="Readable label: 'Good', 'Medium', 'Bad'")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "risk": 1,
                "probability": 0.85,
                "class_label": "Bad"
            }
        }
    )