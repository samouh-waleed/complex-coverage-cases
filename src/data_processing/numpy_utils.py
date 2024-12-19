import numpy as np
from typing import Optional, Tuple, Union, List
from functools import wraps

def validate_array(func):
    """Decorator to validate numpy array inputs."""
    @wraps(func)
    def wrapper(arr, *args, **kwargs):
        if not isinstance(arr, np.ndarray):
            arr = np.array(arr)
        return func(arr, *args, **kwargs)
    return wrapper

class NumpyProcessor:
    """Complex numpy operations demonstrator."""
    
    @staticmethod
    @validate_array
    def matrix_operations(
        arr: np.ndarray,
        operation: str
    ) -> Union[np.ndarray, float]:
        """Perform various matrix operations."""
        if operation == 'eigenvalues':
            return np.linalg.eigvals(arr)
        elif operation == 'inverse':
            return np.linalg.inv(arr)
        elif operation == 'determinant':
            return np.linalg.det(arr)
        elif operation == 'trace':
            return np.trace(arr)
        raise ValueError(f"Unknown operation: {operation}")

    @staticmethod
    @validate_array
    def statistical_analysis(
        arr: np.ndarray,
        axis: Optional[int] = None
    ) -> Dict[str, np.ndarray]:
        """Perform comprehensive statistical analysis."""
        return {
            'mean': np.mean(arr, axis=axis),
            'std': np.std(arr, axis=axis),
            'percentiles': np.percentile(arr, [25, 50, 75], axis=axis),
            'skewness': np.array([
                np.sum((x - np.mean(x))**3)/(len(x)*np.std(x)**3)
                for x in np.atleast_2d(arr)
            ]) if axis is not None else None
        }

    @staticmethod
    def complex_transformations(
        arr: np.ndarray,
        transformations: List[str]
    ) -> Dict[str, np.ndarray]:
        """Apply multiple complex transformations."""
        results = {}
        for transform in transformations:
            if transform == 'fft':
                results['fft'] = np.fft.fft(arr)
            elif transform == 'gradient':
                results['gradient'] = np.gradient(arr)
            elif transform == 'cumsum':
                results['cumsum'] = np.cumsum(arr)
        return results