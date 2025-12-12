from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from src.features.transformers import (
    FeatureSelector, 
    MappingTransformer,
    LogTransformer
)

from src.core.config import (
    MODEL_NUMERIC_COLUMNS,
    MODEL_CATEGORICAL_COLUMNS,
    LOG_TRANSFORMER_FEATURES,
    MODEL_FEATURES,
    settings
)


def create_numeric_pipeline() -> Pipeline:
    """Numeric pipeline: median imputation, log1p (select columns), scaling."""
    return Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('log', LogTransformer(columns=LOG_TRANSFORMER_FEATURES)),
        ('scaler', StandardScaler())
    ])


def create_categorical_pipeline() -> Pipeline:
    """Categorical pipeline: mode imputation, one-hot encoding."""
    return Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(
            drop='first',
            handle_unknown='ignore',
            sparse_output=False
        ))
    ])


def create_preprocessor() -> ColumnTransformer:
    """Apply numeric and categorical pipelines to model features."""
    return ColumnTransformer(
        transformers=[
            ('num', create_numeric_pipeline(), MODEL_NUMERIC_COLUMNS),
            ('cat', create_categorical_pipeline(), MODEL_CATEGORICAL_COLUMNS)
        ],
        remainder='drop'
    )


def create_feature_pipeline() -> Pipeline:
    """Select features, map values, then preprocess."""
    return Pipeline([
        ('selector', FeatureSelector(features=MODEL_FEATURES)),
        ('mapper', MappingTransformer(mappings=settings.mappings)),
        ('preprocessor', create_preprocessor())
    ])


def create_full_pipeline(model) -> Pipeline: 
    """Full pipeline: feature processing and model."""
    return Pipeline([
        ('features', create_feature_pipeline()),
        ('classifier', model)
    ])
