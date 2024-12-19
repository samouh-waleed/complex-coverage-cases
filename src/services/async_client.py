import aiohttp
import asyncio
from typing import Dict, List, Optional, Union, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class AsyncClient:
    """Asynchronous HTTP client with advanced features."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
        self._retry_count = 3
        self._retry_delay = 1

    async def __aenter__(self):
        await self.create_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    async def create_session(self):
        """Create aiohttp session with custom settings."""
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self._session = aiohttp.ClientSession(
            timeout=timeout,
            headers={'User-Agent': 'AsyncClient/1.0'}
        )

    async def close_session(self):
        """Close the aiohttp session."""
        if self._session:
            await self._session.close()
            self._session = None

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Union[Dict, List, str]:
        """Make HTTP request with retry logic."""
        if not self._session:
            await self.create_session()

        url = f"{self.base_url}{endpoint}"
        retries = 0

        while retries < self._retry_count:
            try:
                async with self._session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Request failed: {e}")
                retries += 1
                if retries < self._retry_count:
                    await asyncio.sleep(self._retry_delay * retries)
                else:
                    raise

    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Perform GET request."""
        return await self._make_request('GET', endpoint, params=params)

    async def post(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        """Perform POST request."""
        return await self._make_request('POST', endpoint, json=data)

    async def put(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        """Perform PUT request."""
        return await self._make_request('PUT', endpoint, json=data)

    async def delete(self, endpoint: str) -> Any:
        """Perform DELETE request."""
        return await self._make_request('DELETE', endpoint)
