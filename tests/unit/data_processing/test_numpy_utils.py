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