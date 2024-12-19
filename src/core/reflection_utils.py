import inspect
from typing import Any, Callable, Dict, List, Type, Union
from functools import wraps

class ReflectionUtils:
    """Utility class for reflection and introspection operations."""
    
    @staticmethod
    def get_methods(cls: Type) -> Dict[str, Callable]:
        """Get all methods of a class."""
        return {
            name: method for name, method in inspect.getmembers(cls, predicate=inspect.isfunction)
            if not name.startswith('_')
        }
    
    @staticmethod
    def get_attributes(obj: Any) -> Dict[str, Any]:
        """Get all public attributes of an object."""
        return {
            name: value for name, value in inspect.getmembers(obj)
            if not name.startswith('_') and not callable(value)
        }
    
    @staticmethod
    def create_dynamic_class(
        class_name: str,
        attributes: Dict[str, Any],
        methods: Dict[str, Callable]
    ) -> Type:
        """Create a new class dynamically."""
        return type(class_name, (object,), {**attributes, **methods})
    
    @classmethod
    def create_method_proxy(cls, method: Callable) -> Callable:
        """Create a proxy for a method that logs calls."""
        @wraps(method)
        def proxy(*args, **kwargs):
            print(f"Calling {method.__name__} with args={args}, kwargs={kwargs}")
            result = method(*args, **kwargs)
            print(f"{method.__name__} returned {result}")
            return result
        return proxy
    
    @staticmethod
    def get_callable_signature(func: Callable) -> inspect.Signature:
        """Get the signature of a callable."""
        return inspect.signature(func)
    
    @staticmethod
    def validate_signature(func: Callable, *args: Any, **kwargs: Any) -> bool:
        """Validate if arguments match the function's signature."""
        try:
            inspect.signature(func).bind(*args, **kwargs)
            return True
        except TypeError:
            return False