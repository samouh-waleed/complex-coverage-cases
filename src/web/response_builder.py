from typing import Any, Dict, List, Optional, Union
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ResponseBuilder:
    """Build complex HTTP responses."""
    
    def __init__(self):
        self.status_code = 200
        self.headers: Dict[str, str] = {
            'Content-Type': 'application/json'
        }
        self.body: Dict[str, Any] = {}
        self.cookies: Dict[str, str] = {}

    def set_status(self, status_code: int) -> 'ResponseBuilder':
        """Set response status code."""
        self.status_code = status_code
        return self

    def add_header(
        self,
        key: str,
        value: str
    ) -> 'ResponseBuilder':
        """Add response header."""
        self.headers[key] = value
        return self

    def set_body(
        self,
        data: Union[Dict[str, Any], List[Any]]
    ) -> 'ResponseBuilder':
        """Set response body."""
        self.body = data
        return self

    def add_cookie(
        self,
        name: str,
        value: str,
        expires: Optional[datetime] = None
    ) -> 'ResponseBuilder':
        """Add response cookie."""
        cookie_value = value
        if expires:
            cookie_value += f"; Expires={expires.strftime('%a, %d %b %Y %H:%M:%S GMT')}"
        self.cookies[name] = cookie_value
        return self

    def build(self) -> Dict[str, Any]:
        """Build final response."""
        try:
            # Prepare cookies header
            if self.cookies:
                cookie_strings = [
                    f"{name}={value}"
                    for name, value in self.cookies.items()
                ]
                self.headers['Set-Cookie'] = '; '.join(cookie_strings)

            # Build response
            response = {
                'status_code': self.status_code,
                'headers': self.headers,
                'body': self.body
            }

            # Validate response can be JSON serialized
            json.dumps(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error building response: {str(e)}")
            return {
                'status_code': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'error': 'Internal Server Error',
                    'message': str(e)
                }
            }

    @classmethod
    def create_error_response(
        cls,
        error_message: str,
        status_code: int = 400
    ) -> Dict[str, Any]:
        """Create an error response."""
        return (cls()
            .set_status(status_code)
            .set_body({
                'status': 'error',
                'message': error_message
            })
            .build())

    @classmethod
    def create_success_response(
        cls,
        data: Any,
        status_code: int = 200
    ) -> Dict[str, Any]:
        """Create a success response."""
        return (cls()
            .set_status(status_code)
            .set_body({
                'status': 'success',
                'data': data
            })
            .build())