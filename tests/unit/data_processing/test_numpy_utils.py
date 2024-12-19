import pytest
import numpy as np
from src.data_processing.numpy_utils import NumpyProcessor, validate_array

def test_validate_array_decorator():
    @validate_array
    def test_func(arr):
        return isinstance(arr, np.ndarray)
    
    result = test_func([1, 2, 3])
    assert result is True

def test_matrix_operations():
    arr = np.array([[1, 2], [3, 4]])
    
    # Test eigenvalues
    eigenvals = NumpyProcessor.matrix_operations(arr, 'eigenvalues')
    assert len(eigenvals) == 2
    
    # Test inverse
    inverse = NumpyProcessor.matrix_operations(arr, 'inverse')
    assert np.allclose(np.dot(arr, inverse), np.eye(2))
    
    # Test invalid operation
    with pytest.raises(ValueError):
        NumpyProcessor.matrix_operations(arr, 'invalid_op')

def test_statistical_analysis():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    result = NumpyProcessor.statistical_analysis(arr, axis=1)
    
    assert 'mean' in result
    assert 'std' in result
    assert 'percentiles' in result
    assert len(result['percentiles']) == 3  # 25th, 50th, 75th percentiles

def test_complex_transformations():
    arr = np.array([1, 2, 3, 4])
    transforms = ['fft', 'gradient', 'cumsum']
    result = NumpyProcessor.complex_transformations(arr, transforms)
    
    assert 'fft' in result
    assert 'gradient' in result
    assert 'cumsum' in result
    assert len(result['cumsum']) == len(arr)

# tests/unit/data_processing/test_data_transformers.py
import pytest
import numpy as np
import pandas as pd
from src.data_processing.data_transformers import DataTransformer

@pytest.fixture
def transformer():
    return DataTransformer()

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'numeric': [1, 2, 3, 4, 5],
        'category': ['A', 'B', 'A', 'B', 'C']
    })

def test_scale_features(transformer, sample_data):
    # Test standard scaling
    scaled_standard = transformer.scale_features(
        sample_data[['numeric']],
        method='standard'
    )
    assert np.isclose(scaled_standard['numeric'].mean(), 0, atol=1e-10)
    assert np.isclose(scaled_standard['numeric'].std(), 1, atol=1e-10)
    
    # Test minmax scaling
    scaled_minmax = transformer.scale_features(
        sample_data[['numeric']],
        method='minmax'
    )
    assert scaled_minmax['numeric'].min() == 0
    assert scaled_minmax['numeric'].max() == 1

def test_apply_pca(transformer):
    data = np.random.rand(100, 5)
    transformed, variance = transformer.apply_pca(data, n_components=2)
    
    assert transformed.shape[1] == 2
    assert 0 <= variance <= 1

def test_transform_categorical(transformer, sample_data):
    # Test one-hot encoding
    onehot = transformer.transform_categorical(
        sample_data,
        columns=['category'],
        method='onehot'
    )
    assert 'category_B' in onehot.columns
    assert 'category_C' in onehot.columns
    
    # Test label encoding
    label = transformer.transform_categorical(
        sample_data,
        columns=['category'],
        method='label'
    )
    assert label['category'].nunique() == 3

def test_handle_outliers(transformer):
    data = pd.DataFrame({
        'values': [1, 2, 3, 100, 4, 5, -100]  # Contains outliers
    })
    
    # Test IQR method
    cleaned_iqr = transformer.handle_outliers(data, method='iqr')
    assert cleaned_iqr['values'].max() < 100
    assert cleaned_iqr['values'].min() > -100
    
    # Test zscore method
    cleaned_zscore = transformer.handle_outliers(data, method='zscore')
    assert cleaned_zscore['values'].std() < data['values'].std()