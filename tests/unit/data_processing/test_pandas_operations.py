import pytest
import pandas as pd
import numpy as np
from src.data_processing.pandas_operations import PandasProcessor, handle_missing_data

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'group': ['A', 'A', 'B', 'B', 'C'],
        'value': [1, 2, 3, 4, 5],
        'date': pd.date_range('2023-01-01', periods=5)
    })

def test_aggregate_by_group(sample_df):
    agg_dict = {'value': ['sum', 'mean']}
    result = PandasProcessor.aggregate_by_group(sample_df, ['group'], agg_dict)
    
    assert len(result) == 3  # Three groups: A, B, C
    assert result.loc[result['group'] == 'A', 'value_sum'].iloc[0] == 3
    assert result.loc[result['group'] == 'B', 'value_mean'].iloc[0] == 3.5

def test_handle_missing_data_decorator():
    @handle_missing_data
    def test_func(df):
        return df['non_existent_column'].mean()
    
    result = test_func(pd.DataFrame({'existing': [1, 2, 3]}))
    assert result is None

def test_apply_rolling_calculations(sample_df):
    result = PandasProcessor.apply_rolling_calculations(
        sample_df,
        'value',
        window=2,
        calculations=['mean', 'std']
    )
    
    assert 'value_rolling_mean' in result.columns
    assert 'value_rolling_std' in result.columns
    assert pd.isna(result['value_rolling_mean'].iloc[0])
    assert not pd.isna(result['value_rolling_mean'].iloc[1])

def test_handle_time_series(sample_df):
    result = PandasProcessor.handle_time_series(
        sample_df,
        'date',
        'value',
        freq='D'
    )
    
    assert 'mean' in result.columns
    assert 'count' in result.columns
    assert len(result) == 5  # One row per day

def test_perform_merge_operations():
    left_df = pd.DataFrame({
        'key': ['A', 'B'],
        'value1': [1, 2]
    })
    right_df = pd.DataFrame({
        'key': ['A', 'B'],
        'value2': [3, 4]
    })
    
    result = PandasProcessor.perform_merge_operations(
        left_df,
        right_df,
        merge_columns=['key']
    )
    
    assert len(result) == 2
    assert 'value1' in result.columns
    assert 'value2' in result.columns

def test_perform_merge_operations_invalid_column():
    left_df = pd.DataFrame({'key': ['A']})
    right_df = pd.DataFrame({'different_key': ['A']})
    
    with pytest.raises(ValueError):
        PandasProcessor.perform_merge_operations(
            left_df,
            right_df,
            merge_columns=['key']
        )
