from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.serving.routers import prediction, health


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for credit risk analysis based on Random Forest",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(prediction.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.serving.main:app", host="0.0.0.0", port=8000, reload=True)