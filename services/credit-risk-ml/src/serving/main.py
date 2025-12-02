# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Model de entrada
class PredictRequest(BaseModel):
    age: int
    credit_amount: float
    duration: int


# Model de saída
class PredictResponse(BaseModel):
    risk: str
    probability: float


@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:

    def _test_predict():

        age_factor = max(0, min(1, (request.age - 18) / 50))
        amount_factor = max(0, min(1, request.credit_amount / 10000))
        duration_factor = max(0, min(1, request.duration / 60))

        risk_score = (
            amount_factor * 0.4 + duration_factor * 0.3 + (1 - age_factor) * 0.3
        )
        probability = max(0.1, min(0.99, risk_score))

        risk = "bad" if probability > 0.6 else "good"

        return risk, probability

    risk, probability = _test_predict()

    return PredictResponse(risk=risk, probability=round(probability, 2))


@app.get("/health")
def health():
    return {"status": "ok"}
