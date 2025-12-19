import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Dict, Optional, Union

class MappingTransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-Learn compatible transformer that applies a mapping dictionary
    to translate categorical codes (e.g., 'A11') into readable values.
    
    Enforces strict validation: Raises error if an unknown category is encountered.
    """

    def __init__(self, mappings: Dict[str, Dict[str, str]]):
        """
        Args:
            mappings: Dictionary {col_name: {old_code: new_value}}.
        """
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Applies mapping. Raises ValueError if input data contains codes 
        not present in the mapping dictionary.
        """
        if not isinstance(X, pd.DataFrame):
            raise TypeError("MappingTransformer expects a pandas DataFrame.")

        X_out = X.copy()

        for col, map_dict in self.mappings.items():
            if col in X_out.columns:
                # 1. Strict validation: Check for unknown values before mapping.
                unique_vals = X_out[col].dropna().unique()
                unknown_vals = [val for val in unique_vals if val not in map_dict]
                
                if unknown_vals:
                    raise ValueError(
                        f"Found unknown categories in column '{col}' not present in mapping: {unknown_vals}. "
                        "Update mappings.json or handle new categories."
                    )

                # 2. Apply mapping
                X_out[col] = X_out[col].map(map_dict)
                
        return X_out


class FeatureSelector(BaseEstimator, TransformerMixin):
    """
    Filters the DataFrame to keep only the specified columns.
    Ensures the model receives exactly the expected features.
    """
    def __init__(self, features: List[str]):
        self.features = features

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        # 1. Input type validation
        if not isinstance(X, pd.DataFrame):
            raise TypeError(f"FeatureSelector expects a pandas DataFrame, got {type(X).__name__}")

        # 2. Missing columns validation
        missing_cols = [col for col in self.features if col not in X.columns]
        if missing_cols:
            raise ValueError(f"The following required features are missing in input data: {missing_cols}")

        return X[self.features].copy()


class LogTransformer(BaseEstimator, TransformerMixin):
    """
    Applies log1p transformation to specified columns or the entire input.
    Clip values at 0 to avoid -inf/NaN on negative inputs.
    """
    def __init__(self, columns: Optional[List[str]] = None):
        """
        Args:
            columns: List of column names to transform. 
                     If None, transforms all columns (useful for Pipelines).
        """
        self.columns = columns

    def fit(self, X, y=None):
        """Stateless transformer, no fitting required."""
        return self

    def transform(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Applies transformation handling both DataFrame and Array inputs.
        """
        X_out = X.copy()

        # Case 1: Pandas DataFrame with specific columns
        if hasattr(X_out, 'columns') and self.columns:
            # Validate if columns exist
            missing_cols = [c for c in self.columns if c not in X_out.columns]
            if missing_cols:
                raise ValueError(f"Columns not found for log transformation: {missing_cols}")
            
            X_out[self.columns] = np.log1p(np.clip(X_out[self.columns], 0, None))
            # Return numpy array for sklearn compatibility
            return X_out.values 

        # Case 2: Numpy Array OR DataFrame without specific columns (Transform All)
        return np.log1p(np.clip(X_out, 0, None))