import importlib
import sys
from typing import Any, Dict, Optional
from functools import wraps

class DynamicImporter:
    """Handles dynamic module importing and management."""
    
    @staticmethod
    def import_module(module_path: str) -> Optional[Any]:
        """Dynamically import a module from a string path."""
        try:
            return importlib.import_module(module_path)
        except ImportError as e:
            print(f"Failed to import {module_path}: {e}")
            return None

    @staticmethod
    def import_from_string(import_str: str) -> Any:
        """Import an object from a fully qualified string path."""
        module_path, object_name = import_str.rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, object_name)

    @classmethod
    def lazy_import(cls, module_name: str):
        """Decorator for lazy module importing."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                module = cls.import_module(module_name)
                if module is None:
                    raise ImportError(f"Required module {module_name} not found")
                setattr(wrapper, 'module', module)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def conditional_import(module_name: str, fallback: Any = None) -> Any:
        """Conditionally import a module with fallback."""
        try:
            return importlib.import_module(module_name)
        except ImportError:
            return fallback

class ModuleRegistry:
    """Registry for dynamically loaded modules."""
    
    def __init__(self):
        self._modules: Dict[str, Any] = {}

    def register(self, name: str, module: Any) -> None:
        """Register a module in the registry."""
        self._modules[name] = module

    def get(self, name: str) -> Optional[Any]:
        """Get a module from the registry."""
        return self._modules.get(name)

    def load_module(self, module_path: str) -> Optional[Any]:
        """Load and register a module."""
        module = DynamicImporter.import_module(module_path)
        if module:
            self.register(module_path, module)
        return module