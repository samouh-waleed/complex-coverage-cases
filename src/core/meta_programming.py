from typing import Any, Callable, Dict, Type, TypeVar, Optional
from functools import wraps
import inspect

T = TypeVar('T')

def singleton(cls: Type[T]) -> Type[T]:
    """Singleton decorator for classes."""
    _instances: Dict[Type[T], T] = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs) -> T:
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    
    return get_instance

def debug_calls(func: Callable) -> Callable:
    """Decorator to debug function calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        call_args = ", ".join([
            *[str(arg) for arg in args],
            *[f"{k}={v}" for k, v in kwargs.items()]
        ])
        print(f"Calling {func.__name__}({call_args})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

class MethodRegistryMetaclass(type):
    """Metaclass for registering methods with specific attributes."""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        registry = {}
        
        for key, value in namespace.items():
            if hasattr(value, '_register'):
                registry[key] = value
        
        namespace['_registry'] = registry
        return super().__new__(mcs, name, bases, namespace)

def register_method(name: Optional[str] = None) -> Callable:
    """Decorator to register methods in the registry."""
    def decorator(func: Callable) -> Callable:
        func._register = True
        func._registry_name = name or func.__name__
        return func
    return decorator

class AutoPropertyMetaclass(type):
    """Metaclass for automatically creating properties from annotations."""
    
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        annotations = namespace.get('__annotations__', {})
        
        for attr_name, attr_type in annotations.items():
            if not attr_name.startswith('_'):
                private_name = f'_{attr_name}'
                
                def getter(self, name=private_name):
                    return getattr(self, name)
                
                def setter(self, value, name=private_name, typ=attr_type):
                    if not isinstance(value, typ):
                        raise TypeError(f"Expected {typ.__name__}, got {type(value).__name__}")
                    setattr(self, name, value)
                
                namespace[private_name] = None
                namespace[attr_name] = property(getter, setter)
        
        return super().__new__(mcs, name, bases, namespace)
