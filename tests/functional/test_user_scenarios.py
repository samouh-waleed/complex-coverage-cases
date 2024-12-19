import asyncio
from Reop3.src.services.async_client import AsyncClient
import pytest
from src.core.meta_programming import singleton
from src.data_processing.data_transformers import DataTransformer
from src.services.cache_manager import CacheManager

@pytest.mark.functional
class TestUserScenarios:
    def test_data_transformation_scenario(self):
        """Test complete data transformation user scenario."""
        # Setup
        transformer = DataTransformer()
        cache = CacheManager('redis://localhost:6379')
        
        # 1. User uploads data
        input_data = {
            'numeric_data': [1, 2, 3, 4, 5],
            'categories': ['A', 'B', 'A', 'C', 'B']
        }
        
        # 2. Data transformation
        try:
            # Scale numeric data
            scaled = transformer.scale_features(
                input_data['numeric_data'],
                method='standard'
            )
            
            # Transform categories
            encoded = transformer.transform_categorical(
                input_data['categories'],
                method='onehot'
            )
            
            # Cache results
            cache.set('transformation_results', {
                'scaled': scaled,
                'encoded': encoded
            })
            
            # 3. Retrieve results
            results = cache.get('transformation_results')
            assert results is not None
            assert 'scaled' in results
            assert 'encoded' in results
            
        finally:
            # Cleanup
            cache.delete('transformation_results')

    @pytest.mark.asyncio
    async def test_async_processing_scenario(self):
        """Test async processing user scenario."""
        # Implementation of async processing scenario
        async with AsyncClient('http://api.example.com') as client:
            # 1. User initiates async process
            process_id = await client.post('/start-process')
            
            # 2. Poll for results
            max_attempts = 5
            attempt = 0
            result = None
            
            while attempt < max_attempts:
                status = await client.get(f'/status/{process_id}')
                if status['completed']:
                    result = status['result']
                    break
                attempt += 1
                await asyncio.sleep(1)
            
            assert result is not None
            assert 'data' in result