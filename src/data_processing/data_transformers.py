from typing import Any, Dict, List, Optional, Union
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from typing import Any, Dict, List, Optional, Union, Tuple


class DataTransformer:
    """Complex data transformation operations."""
    
    def __init__(self):
        self.scalers: Dict[str, Any] = {
            'standard': StandardScaler(),
            'minmax': MinMaxScaler()
        }
        self.pca = None

    def scale_features(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        method: str = 'standard',
        columns: Optional[List[str]] = None
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Scale features using various methods."""
        if method not in self.scalers:
            raise ValueError(f"Unknown scaling method: {method}")
        
        if isinstance(data, pd.DataFrame):
            cols_to_scale = columns or data.select_dtypes(include=[np.number]).columns
            scaled_data = data.copy()
            scaled_data[cols_to_scale] = self.scalers[method].fit_transform(data[cols_to_scale])
            return scaled_data
        else:
            return self.scalers[method].fit_transform(data)

    def apply_pca(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        n_components: Optional[int] = None,
        variance_ratio: Optional[float] = None
    ) -> Tuple[Union[pd.DataFrame, np.ndarray], float]:
        """Apply PCA transformation."""
        if n_components is None and variance_ratio is not None:
            n_components = self._find_components_for_variance(data, variance_ratio)
        
        self.pca = PCA(n_components=n_components)
        transformed_data = self.pca.fit_transform(data)
        
        if isinstance(data, pd.DataFrame):
            return (
                pd.DataFrame(
                    transformed_data,
                    columns=[f'PC{i+1}' for i in range(transformed_data.shape[1])]
                ),
                self.pca.explained_variance_ratio_.sum()
            )
        return transformed_data, self.pca.explained_variance_ratio_.sum()

    def _find_components_for_variance(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        target_variance: float
    ) -> int:
        """Find number of components needed for target variance."""
        temp_pca = PCA()
        temp_pca.fit(data)
        cumsum = np.cumsum(temp_pca.explained_variance_ratio_)
        n_components = np.argmax(cumsum >= target_variance) + 1
        return n_components

    def transform_categorical(
        self,
        data: pd.DataFrame,
        columns: List[str],
        method: str = 'onehot'
    ) -> pd.DataFrame:
        """Transform categorical variables using various methods."""
        result = data.copy()
        
        if method == 'onehot':
            for column in columns:
                dummies = pd.get_dummies(
                    result[column],
                    prefix=column,
                    drop_first=True
                )
                result = pd.concat([result, dummies], axis=1)
                result.drop(column, axis=1, inplace=True)
        
        elif method == 'label':
            for column in columns:
                result[column] = pd.factorize(result[column])[0]
                
        elif method == 'binary':
            for column in columns:
                unique_values = result[column].unique()
                if len(unique_values) != 2:
                    raise ValueError(f"Column {column} must have exactly 2 unique values for binary encoding")
                result[column] = (result[column] == unique_values[0]).astype(int)
                
        return result

    def handle_outliers(
        self,
        data: Union[pd.DataFrame, np.ndarray],
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Handle outliers using various methods."""
        if isinstance(data, pd.DataFrame):
            result = data.copy()
            numeric_cols = result.select_dtypes(include=[np.number]).columns
            
            if method == 'iqr':
                for col in numeric_cols:
                    Q1 = result[col].quantile(0.25)
                    Q3 = result[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    result[col] = result[col].clip(lower_bound, upper_bound)
                    
            elif method == 'zscore':
                for col in numeric_cols:
                    z_scores = np.abs((result[col] - result[col].mean()) / result[col].std())
                    result[col] = result[col].mask(z_scores > threshold, result[col].mean())
                    
            return result
        else:
            if method == 'iqr':
                Q1 = np.percentile(data, 25, axis=0)
                Q3 = np.percentile(data, 75, axis=0)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                return np.clip(data, lower_bound, upper_bound)
            
            elif method == 'zscore':
                z_scores = np.abs((data - np.mean(data, axis=0)) / np.std(data, axis=0))
                mask = z_scores > threshold
                data[mask] = np.mean(data, axis=0)[mask[0]]
                return data