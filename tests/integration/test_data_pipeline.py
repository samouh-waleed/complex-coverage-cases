import pytest
import pandas as pd
import numpy as np
from src.data_processing.pandas_operations import PandasProcessor
from src.data_processing.numpy_utils import NumpyProcessor
from src.data_processing.data_transformers import DataTransformer

@pytest.fixture
def complex_dataset():
    # Create a complex dataset for integration testing
    np.random.seed(42)
    return pd.DataFrame({
        'numeric': np.random.randn(100),
        'categorical': np.random.choice(['A', 'B', 'C'], 100),
        'datetime': pd.date_range('2023-01-01', periods=100)
    })

@pytest.mark.integration
def test_full_data_pipeline(complex_dataset):
    # Test complete data processing pipeline
    
    # 1. Initial data transformations
    transformer = DataTransformer()
    scaled_data = transformer.scale_features(
        complex_dataset[['numeric']],
        method='standard'
    )
    
    # 2. Categorical transformations
    encoded_data = transformer.transform_categorical(
        complex_dataset,
        columns=['categorical'],
        method='onehot'
    )
    
    # 3. Apply numpy operations
    numpy_processor = NumpyProcessor()
    stats = numpy_processor.statistical_analysis(
        scaled_data.values
    )
    
    # Assertions
    assert 'mean' in stats
    assert 'std' in stats
    assert encoded_data.shape[1] > complex_dataset.shape[1]
