import pytest
from src.core.dynamic_imports import DynamicImporter
from src.data_processing.pandas_operations import PandasProcessor
from src.services.async_client import AsyncClient
from src.web.request_handler import RequestHandler

@pytest.mark.functional
class TestEndToEnd:
    @pytest.fixture(autouse=True)
    async def setup(self):
        # Setup test environment
        self.importer = DynamicImporter()
        self.processor = PandasProcessor()
        self.handler = RequestHandler()
        self.client = AsyncClient('http://test-api.example.com')
        
        yield
        
        # Cleanup
        await self.client.close_session()

    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        # Test complete application workflow
        
        # 1. Dynamic module loading
        pandas = self.importer.import_module('pandas')
        assert pandas is not None
        
        # 2. Data processing
        test_data = pandas.DataFrame({
            'value': range(10),
            'group': ['A', 'B'] * 5
        })
        
        processed_data = self.processor.aggregate_by_group(
            test_data,
            ['group'],
            {'value': ['sum', 'mean']}
        )
        
        # 3. API interaction
        async with self.client as client:
            response = await client.post(
                '/process',
                data=processed_data.to_dict()
            )
            assert response['status'] == 'success'
        
        # 4. Request handling
        final_response = self.handler.handle_request({
            'method': 'POST',
            'path': '/api/results',
            'headers': {'Content-Type': 'application/json'},
            'body': response
        })
        
        assert final_response['status_code'] == 200