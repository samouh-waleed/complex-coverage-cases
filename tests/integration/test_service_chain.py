import pytest
import aiohttp
import asyncio
from src.services.async_client import AsyncClient
from src.services.data_fetcher import DataFetcher
from src.services.cache_manager import CacheManager

@pytest.mark.asyncio
async def test_service_integration():
    # Test integration between async client, data fetcher, and cache
    async with AsyncClient('https://api.example.com') as client:
        # 1. Fetch data
        data = await client.get('/test-endpoint')
        
        # 2. Process with data fetcher
        fetcher = DataFetcher()
        processed_data = fetcher.process_data(data)
        
        # 3. Cache results
        cache_manager = CacheManager('redis://localhost:6379')
        cache_key = 'test_integration'
        await cache_manager.set(cache_key, processed_data)
        
        # 4. Verify cached data
        cached_result = await cache_manager.get(cache_key)
        assert cached_result == processed_data