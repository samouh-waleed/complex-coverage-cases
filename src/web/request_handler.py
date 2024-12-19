from typing import Dict, Any, Optional, Union, Callable
import json
import logging
from functools import wraps
import traceback

logger = logging.getLogger(__name__)

def validate_request(schema: Dict[str, type]):
    """Decorator to validate request data."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, request_data: Dict[str, Any], *args, **kwargs):
            # Validate required fields and types
            for field, expected_type in schema.items():
                if field not in request_data:
                    raise ValueError(f"Missing required field: {field}")
                if not isinstance(request_data[field], expected_type):
                    raise TypeError(
                        f"Invalid type for {field}. "
                        f"Expected {expected_type}, got {type(request_data[field])}"
                    )
            return func(self, request_data, *args, **kwargs)
        return wrapper
    return decorator

class RequestHandler:
    """Handle complex web requests."""
    
    def __init__(self):
        self.middlewares: List[Callable] = []
        self.error_handlers: Dict[type, Callable] = {}

    def add_middleware(self, middleware: Callable) -> None:
        """Add middleware to the request processing pipeline."""
        self.middlewares.append(middleware)

    def register_error_handler(
        self,
        exception_type: type,
        handler: Callable
    ) -> None:
        """Register an error handler for specific exception type."""
        self.error_handlers[exception_type] = handler

    def _apply_middlewares(
        self,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply all middlewares to request data."""
        data = request_data.copy()
        for middleware in self.middlewares:
            try:
                data = middleware(data)
            except Exception as e:
                logger.error(f"Middleware error: {str(e)}")
                raise
        return data

    @validate_request({
        'method': str,
        'path': str,
        'headers': dict
    })
    def handle_request(
        self,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process incoming request with error handling."""
        try:
            # Apply middlewares
            processed_data = self._apply_middlewares(request_data)
            
            # Route request
            if processed_data['method'] == 'GET':
                return self.handle_get(processed_data)
            elif processed_data['method'] == 'POST':
                return self.handle_post(processed_data)
            elif processed_data['method'] == 'PUT':
                return self.handle_put(processed_data)
            elif processed_data['method'] == 'DELETE':
                return self.handle_delete(processed_data)
                
            raise ValueError(f"Unsupported method: {processed_data['method']}")
            
        except Exception as e:
            return self._handle_error(e)

    def _handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle errors with registered error handlers."""
        for error_type, handler in self.error_handlers.items():
            if isinstance(error, error_type):
                return handler(error)
                
        # Default error handling
        logger.error(f"Unhandled error: {traceback.format_exc()}")
        return {
            'status': 'error',
            'message': str(error),
            'type': error.__class__.__name__
        }
