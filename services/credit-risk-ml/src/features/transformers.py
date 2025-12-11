import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from typing import Dict, List

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
        """
        fit does nothing here because the mapping is static (comes from JSON/config).
        However, the method MUST exist for Pipeline compatibility.
        """
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
    
    def fit(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        missing_cols = [col for col in self.features if col not in X.columns]

        if missing_cols:
            raise ValueError(f"The following required features are missing in input data: {missing_cols}")

        return X[self.features].copy()