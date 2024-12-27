import requests
from typing import Dict, List, Optional, Union
import concurrent.futures
import pandas as pd
import json
from functools import wraps
import time

def retry_on_failure(max_retries: int = 3, delay: int = 1):
    """Decorator for retrying failed requests."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.RequestException, ConnectionError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    time.sleep(delay * retries)
            return None
        return wrapper
    return decorator

class DataFetcher:
    """Handle complex data fetching operations."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def process_data(self, data: Dict) -> Dict:
    # For now, do nothing fancy, just return it
        return data
    
    @retry_on_failure(max_retries=3)
    def fetch_json_data(
        self,
        url: str,
        params: Optional[Dict] = None
    ) -> Dict:
        """Fetch JSON data from API."""
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_pandas_data(
        self,
        url: str,
        format: str = 'csv'
    ) -> pd.DataFrame:
        """Fetch data and convert to DataFrame."""
        if format == 'csv':
            return pd.read_csv(url)
        elif format == 'excel':
            return pd.read_excel(url)
        elif format == 'json':
            return pd.read_json(url)
        raise ValueError(f"Unsupported format: {format}")

    @retry_on_failure(max_retries=3)
    def fetch_bulk_data(
        self,
        urls: List[str],
        parallel: bool = True
    ) -> List[Dict]:
        """Fetch data from multiple URLs."""
        if parallel:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self.fetch_json_data, url)
                    for url in urls
                ]
                return [f.result() for f in futures]
        return [self.fetch_json_data(url) for url in urls]

    def fetch_paginated_data(
        self,
        url: str,
        page_param: str = 'page',
        limit_param: str = 'limit',
        limit: int = 100
    ) -> List[Dict]:
        """Fetch paginated data."""
        all_data = []
        page = 1
        
        while True:
            params = {
                page_param: page,
                limit_param: limit
            }
            
            data = self.fetch_json_data(url, params=params)
            if not data:
                break
                
            all_data.extend(data)
            page += 1
            
        return all_data
