import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Dict


class MappingTransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-Learn compatible transformer that applies a mapping dictionary
    to translate categorical codes (e.g., 'A11') into readable values (e.g., 'less_0').
    """

    def __init__(self, mappings: Dict[str, Dict[str, str]]):
        """
        Args:
            mappings: Dictionary where the key is the column name and the value
                      is another dictionary {old_code: new_value}.
        """
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the value replacements.
        """
        X_out = X.copy()

        for col, map_dict in self.mappings.items():
            if col in X_out.columns:
                X_out[col] = X_out[col].replace(map_dict)

        return X_out


class FeatureSelector(BaseEstimator, TransformerMixin):
    """
    Filters the DataFrame to keep only the specified columns.
    Essential to ensure the model only receives the features it was trained to use.
    """
    def __init__(self, features: List[str]):
        """
        Args:
            features: List of column names to keep (e.g., NUMERIC + CATEGORICAL features).
        """
        self.features = features

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        missing_cols = [col for col in self.features if col not in X.columns]

        if missing_cols:
            raise ValueError(f"The following required features are missing in input data: {missing_cols}")

        return X[self.features].copy()


class LogTransformer(BaseEstimator, TransformerMixin):
    """
    Apply log1p transformation to specified columns.
    Works with both DataFrame and ndarray inputs.
    """
    def __init__(self, columns: List[str], column_order: List[str] = None):
        """
        Args:
            columns: List of column names to apply log transformation.
            column_order: Optional list specifying the order of columns when X is an ndarray.
                        If None and X is an ndarray, assumes columns are in the same order as self.columns.
        """
        self.columns = columns
        self.column_order = column_order
        self.column_indices_: List[int] = []

    def fit(self, X, y=None):
        """
        Store column indices based on input type.
        """
        if hasattr(X, 'columns'):
            self.column_indices_ = [
                list(X.columns).index(col) 
                for col in self.columns 
                if col in X.columns
            ]
        else:
            if self.column_order is not None:
                self.column_indices_ = [
                    self.column_order.index(col) 
                    for col in self.columns 
                    if col in self.column_order
                ]
            else:
                self.column_indices_ = list(range(len(self.columns)))
        return self

    def transform(self, X) -> np.ndarray:
        """
        Apply log1p to specified columns, clipping negatives at 0.
        Accepts DataFrame or ndarray.
        """
        if hasattr(X, 'columns'):
            X_out = X.copy()
            for col in self.columns:
                if col not in X_out.columns:
                    raise ValueError(f"Column '{col}' not found in input DataFrame.")
                X_out[col] = np.log1p(np.clip(X_out[col], 0, None))
            return X_out.values
        else:
            X_out = np.array(X, dtype=float, copy=True)
            for idx in self.column_indices_:
                if idx >= X_out.shape[1]:
                    continue  
                X_out[:, idx] = np.log1p(np.clip(X_out[:, idx], 0, None))
            return X_out