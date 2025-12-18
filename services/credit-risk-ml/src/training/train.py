import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from loguru import logger

from src.core.config import settings, TARGET_COLUMN
from src.data.ingestion import download_dataset
from src.data.io import load_raw_data, save_model
from src.features.pipeline import create_full_pipeline

def train_model():
    logger.info("[TRAIN] Starting training process...")

    # 1. Data Ingestion and Loading
    raw_path = download_dataset(overwrite=False)
    df = load_raw_data(raw_path)

    # 2. Data Preparation (Split X/y)
    logger.info("[TRAIN] Splitting features and target...")
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    # Target transformation (German Credit: 1=good, 2=bad -> 0=good, 1=bad)
    y = y.map({1: 0, 2: 1})
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    logger.info("[TRAIN] Training data: %d samples", X_train.shape[0])
    logger.info("[TRAIN] Test data: %d samples", X_test.shape[0])

    # 4. Model and Pipeline Definition
    rf_model = RandomForestClassifier(
        n_estimators=200, 
        max_depth=10, 
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )
    
    # Create the complete pipeline using the pipeline factory function
    pipeline = create_full_pipeline(rf_model)

    # 5. Fitting
    logger.info("[TRAIN] Treinando o Pipeline completo...")
    pipeline.fit(X_train, y_train)

    # 6. Evaluation
    logger.info("[TRAIN] Evaluating metrics...")
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    logger.info("="*40)
    logger.info("CLASSIFICATION REPORT")
    logger.info("="*40)
    classification_rep = classification_report(y_test, y_pred)
    for line in classification_rep.split('\n'):
        logger.info(line)
    
    auc = roc_auc_score(y_test, y_proba)
    logger.info("ROC-AUC Score: %.4f", auc)
    logger.info("="*40)

    # Save metrics as JSON for MLOps
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    metrics = {
        "accuracy": report_dict["accuracy"],
        "precision_bad": report_dict["1"]["precision"],
        "recall_bad": report_dict["1"]["recall"],
        "f1_bad": report_dict["1"]["f1-score"],
        "roc_auc": auc
    }

    reports_dir = settings.root_dir / "reports"
    reports_dir.mkdir(exist_ok=True)

    metrics_path = reports_dir / "metrics.json"
    
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.info("[TRAIN] Metrics saved at: %s", metrics_path)

    # 7. Persistence (Save)
    model_path = settings.models_prod_dir / "model.pkl"
    save_model(pipeline, model_path)
    logger.info("[TRAIN] Training completed. Artifact saved at: %s", model_path)

if __name__ == "__main__":
    train_model()