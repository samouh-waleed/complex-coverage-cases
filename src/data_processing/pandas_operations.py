import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional
from functools import wraps

def handle_missing_data(func):
    """Decorator to handle missing data in DataFrames."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            print(f"Missing column: {e}")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None
    return wrapper

class PandasProcessor:
    """Complex pandas operations demonstrator."""
    
    @staticmethod
    @handle_missing_data
    def aggregate_by_group(
        df: pd.DataFrame,
        group_cols: List[str],
        agg_dict: Dict[str, List[str]]
    ) -> pd.DataFrame:
        """Perform complex groupby aggregation."""
        return df.groupby(group_cols).agg(agg_dict).reset_index()

    @staticmethod
    def apply_rolling_calculations(
        df: pd.DataFrame,
        column: str,
        window: int,
        calculations: List[str]
    ) -> pd.DataFrame:
        """Apply multiple rolling window calculations."""
        result = df.copy()
        for calc in calculations:
            if calc == 'mean':
                result[f'{column}_rolling_mean'] = df[column].rolling(window).mean()
            elif calc == 'std':
                result[f'{column}_rolling_std'] = df[column].rolling(window).std()
            elif calc == 'sum':
                result[f'{column}_rolling_sum'] = df[column].rolling(window).sum()
        return result

    @staticmethod
    def handle_time_series(
        df: pd.DataFrame,
        date_column: str,
        value_column: str,
        freq: str = 'D'
    ) -> pd.DataFrame:
        """Process time series data with various frequencies."""
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.set_index(date_column)
        df = df.resample(freq)[value_column].agg(['mean', 'min', 'max', 'count'])
        return df.reset_index()

    @staticmethod
    def perform_merge_operations(
        left_df: pd.DataFrame,
        right_df: pd.DataFrame,
        merge_columns: List[str],
        merge_type: str = 'left'
    ) -> pd.DataFrame:
        """Perform complex merge operations with validation."""
        # Validate merge columns exist
        for col in merge_columns:
            if col not in left_df.columns or col not in right_df.columns:
                raise ValueError(f"Merge column {col} not found in both DataFrames")
        
        # Perform merge
        merged_df = pd.merge(
            left_df,
            right_df,
            on=merge_columns,
            how=merge_type,
            validate='1:1'  # Ensure no duplicate matches
        )
        
        return merged_df