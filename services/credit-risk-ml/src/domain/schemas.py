from pydantic import BaseModel, Field, ConfigDict


class PredictionInput(BaseModel):
    credit_amount: float = Field(..., gt=0, description="Credit amount applied for")
    duration_in_month: int = Field(
        ..., gt=0, description="Duration of the credit in months"
    )
    age_in_years: int = Field(
        ..., ge=18, le=120, description="Age of the applicant in years"
    )
    installment_rate_percent: int = Field(
        ..., ge=1, le=4, description="Installment rate as percent of disposable income"
    )
    present_residence_since: int = Field(
        ..., ge=1, description="Number of years at current residence"
    )
    checking_account_status: str = Field(
        ..., description="Status of existing checking account"
    )
    credit_history: str = Field(..., description="Credit history of the applicant")
    purpose: str = Field(..., description="Purpose of the credit application")
    property: str = Field(..., description="Type of property")
    savings_account_bonds: str = Field(
        ..., description="Status of savings account or bonds"
    )
    present_employment_since: str = Field(
        ..., description="Duration of present employment"
    )
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "credit_amount": 3000.0,
                "duration_in_month": 24,
                "age_in_years": 35,
                "installment_rate_percent": 3,
                "present_residence_since": 2,
                "checking_account_status": "A11",
                "credit_history": "A32",
                "purpose": "A40",
                "property": "A121",
                "savings_account_bonds": "A61",
                "present_employment_since": "A73",
            }
        }
    )


class PredictionOutput(BaseModel):
    risk: int = Field(..., description="Predicted risk class (0=Good, 1=Bad)")
    probability: float = Field(
        ..., description="Probability of the positive class (Bad Risk)"
    )
    class_label: str = Field(..., description="Readable label: 'Good' or 'Bad'")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"risk": 1, "probability": 0.85, "class_label": "Bad"}
        }
    )
