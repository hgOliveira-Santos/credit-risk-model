import json
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline
from loguru import logger

# Import centralized config and hyperparameters
from src.core.config import settings, TARGET_COLUMN, MODEL_PARAMS
from src.data.ingestion import download_dataset
from src.data.io import load_raw_data, save_model
from src.features.pipeline import create_full_pipeline


def load_and_prepare_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Orchestrates data ingestion, loading, cleaning, and splitting.
    """
    logger.info("[DATA] Starting data preparation...")

    # 1. Data ingestion (download if necessary)
    raw_path = download_dataset(overwrite=False)
    df = load_raw_data(raw_path)

    # 2. Separate features and target column
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    # 3. Target Transformation
    y = y.map({1: 0, 2: 1})

    # 4. Splitting
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    logger.info(
        f"[DATA] Split complete. Train shape: {X_train.shape}, Test shape: {X_test.shape}"
    )
    return X_train, X_test, y_train, y_test


def train_pipeline(X_train: pd.DataFrame, y_train: pd.Series) -> Pipeline:
    """
    Instantiates the model using config params and fits the pipeline.
    """
    logger.info("[TRAIN] Initializing model with params: {}", MODEL_PARAMS)

    clf = RandomForestClassifier(
        n_jobs=-1,
        **MODEL_PARAMS,
    )

    pipeline = create_full_pipeline(clf)

    logger.info("[TRAIN] Fitting pipeline...")
    pipeline.fit(X_train, y_train)

    return pipeline


def evaluate_model(
    pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series
) -> Dict[str, Any]:
    """
    Calculates and logs performance metrics.
    """
    logger.info("[EVAL] Evaluating model performance...")

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    # Metrics calculation
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    auc_score = roc_auc_score(y_test, y_proba)

    # Collect main metrics for MLOps/logging
    metrics = {
        "accuracy": report_dict["accuracy"],
        "precision_bad": report_dict["1"]["precision"],
        "recall_bad": report_dict["1"]["recall"],
        "f1_bad": report_dict["1"]["f1-score"],
        "roc_auc": auc_score,
    }

    # Log principal metrics
    logger.info(f"ROC-AUC: {auc_score:.4f}")
    logger.info(f"Recall (Bad Class): {metrics['recall_bad']:.4f}")

    return metrics


def save_artifacts(pipeline: Pipeline, metrics: Dict[str, Any]):
    """
    Saves the trained model and metadata JSON with versioning information.
    """
    # 1. Define output paths for models and reports
    models_dir = settings.models_prod_dir
    reports_dir = settings.root_dir / "reports"

    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 2. Save the model (pickle format)
    model_filename = f"model_{timestamp}.pkl"
    model_path = models_dir / model_filename
    save_model(pipeline, model_path)

    # For convenience: also save model as 'model.pkl' for easy API consumption
    save_model(pipeline, models_dir / "model.pkl")

    # 3. Save metadata (JSON describing model, params, metrics, etc.)
    metadata = {
        "timestamp": timestamp,
        "model_type": "RandomForestClassifier",
        "parameters": MODEL_PARAMS,
        "metrics": metrics,
        "artifact_path": str(model_path),
    }

    metadata_path = reports_dir / f"metadata_{timestamp}.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

    # Save metrics.json for easy CI/CD consumption
    with open(reports_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    logger.success(f"[PERSISTENCE] Artifacts saved. Metadata: {metadata_path}")


def main():
    try:
        # 1. Data preparation (ingest, clean, split)
        X_train, X_test, y_train, y_test = load_and_prepare_data()

        # 2. Model training (fit pipeline)
        pipeline = train_pipeline(X_train, y_train)

        # 3. Evaluation (metrics calculation)
        metrics = evaluate_model(pipeline, X_test, y_test)

        # 4. Save model and metadata artifacts
        save_artifacts(pipeline, metrics)

    except Exception as e:
        logger.exception("[TRAIN] Training pipeline failed.")
        raise e


if __name__ == "__main__":
    main()
