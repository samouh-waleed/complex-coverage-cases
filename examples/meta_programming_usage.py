"""Example of meta-programming features and patterns."""
from typing import Any, Dict, Type, TypeVar
from functools import wraps

T = TypeVar('T')

def singleton(cls: Type[T]) -> Type[T]:
    """Singleton decorator example."""
    instances: Dict[Type[T], T] = {}
    
    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

class MetaLogger(type):
    """Metaclass that logs class creation and method calls."""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        # Log class creation
        print(f"Creating class: {name}")
        
        # Wrap methods with logging
        for key, value in namespace.items():
            if callable(value) and not key.startswith('__'):
                namespace[key] = mcs.log_method(value)
        
        return super().__new__(mcs, name, bases, namespace)
    
    @staticmethod
    def log_method(method):
        """Wrap method with logging."""
        @wraps(method)
        def wrapper(*args, **kwargs):
            print(f"Calling method: {method.__name__}")
            result = method(*args, **kwargs)
            print(f"Method {method.__name__} returned: {result}")
            return result
        return wrapper

@singleton
class Configuration:
    """Example singleton class."""
    
    def __init__(self):
        self.settings: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

class LoggedClass(metaclass=MetaLogger):
    """Example class using the logging metaclass."""
    
    def process_data(self, data: Any) -> str:
        return f"Processed: {data}"
    
    def validate(self, value: Any) -> bool:
        return bool(value)

def example_usage():
    """Example usage of meta-programming features."""
    # Singleton example
    config1 = Configuration()
    config2 = Configuration()
    assert config1 is config2
    
    config1.set('api_key', '12345')
    print(f"Config from instance 2: {config2.get('api_key')}")
    
    # Metaclass example
    logged = LoggedClass()
    logged.process_data("test")
    logged.validate(True)

if __name__ == "__main__":
    example_usage()