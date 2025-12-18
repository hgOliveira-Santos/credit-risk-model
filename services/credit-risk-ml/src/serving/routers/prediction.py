import pandas as pd
import logger
from fastapi import APIRouter, Depends, HTTPException

from src.domain.schemas import PredictionInput, PredictionOutput
from src.serving.dependencies import get_model
from src.core.config import RISK_THRESHOLD_HIGH, RISK_THRESHOLD_LOW

router = APIRouter()

def get_risk_label(probability: float) -> str:
    if probability < RISK_THRESHOLD_LOW:
        return "Good"
    elif probability < RISK_THRESHOLD_HIGH:
        return "Medium"
    else: 
        return "Bad"

@router.post("/predict", responde_model=PredictionOutput)
def predict_credit_risk(
    input_data: PredictionInput,
    model: Depends(get_model)
): 
    try:
        input_df = pd.DataFrame([input_data.model_dump()])
        binary_prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        label = get_risk_label(probability)

        return PredictionOutput(
            risk=int(binary_prediction),
            probability=float(probability),
            class_label=label
        )
    except Exception as e:
        logger.error(f"[PREDICTION ERROR] {e}")
        raise HTTPException(status_code=500, detail="Prediction failed: " + str(e))    