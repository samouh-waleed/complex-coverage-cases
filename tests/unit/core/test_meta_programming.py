import pytest
import pandas as pd
import numpy as np
from src.data_processing.pandas_operations import PandasProcessor

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'group': ['A', 'A', 'B', 'B'],
        'value': [1, 2, 3, 4]
    })

def test_aggregate_by_group(sample_df):
    agg_dict = {'value': ['sum', 'mean']}
    result = PandasProcessor.aggregate_by_group(
        sample_df,
        ['group'],
        agg_dict
    )
    
    assert len(result) == 2
    assert result.loc[result['group'] == 'A', 'value_sum'].iloc[0] == 3