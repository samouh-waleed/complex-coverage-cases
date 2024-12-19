import pytest
from src.web.request_handler import RequestHandler
from src.web.response_builder import ResponseBuilder

@pytest.mark.integration
def test_web_request_flow():
    # Test complete web request/response flow
    handler = RequestHandler()
    builder = ResponseBuilder()
    
    # 1. Create request
    request_data = {
        'method': 'POST',
        'path': '/api/test',
        'headers': {'Content-Type': 'application/json'},
        'body': {'test': 'data'}
    }
    
    # 2. Handle request
    response = handler.handle_request(request_data)
    
    # 3. Build response
    final_response = builder.set_status(200)\
        .set_body(response)\
        .add_header('X-Test', 'Integration')\
        .build()
    
    # Assertions
    assert final_response['status_code'] == 200
    assert 'X-Test' in final_response['headers']