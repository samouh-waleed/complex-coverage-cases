"""Example of dynamic imports and runtime module loading."""
import importlib
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DynamicLoader:
    """Demonstrates dynamic module loading patterns."""
    
    def __init__(self):
        self.loaded_modules: Dict[str, Any] = {}
        
    def load_module(self, module_name: str) -> Optional[Any]:
        """Dynamically load a module at runtime."""
        try:
            if module_name not in self.loaded_modules:
                module = importlib.import_module(module_name)
                self.loaded_modules[module_name] = module
                logger.info(f"Successfully loaded module: {module_name}")
                return module
            return self.loaded_modules[module_name]
        except ImportError as e:
            logger.error(f"Failed to load module {module_name}: {e}")
            return None

    def load_module_attribute(self, module_name: str, attribute: str) -> Optional[Any]:
        """Load a specific attribute from a module."""
        module = self.load_module(module_name)
        if module and hasattr(module, attribute):
            return getattr(module, attribute)
        return None

    @staticmethod
    def load_from_string(import_string: str) -> Optional[Any]:
        """Load an object from a fully qualified string path."""
        try:
            module_path, object_name = import_string.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, object_name)
        except (ImportError, AttributeError) as e:
            logger.error(f"Failed to load {import_string}: {e}")
            return None

def example_usage():
    """Example usage of dynamic loading."""
    loader = DynamicLoader()
    
    # Load built-in module
    json_module = loader.load_module('json')
    if json_module:
        data = json_module.dumps({'test': 'data'})
        print(f"JSON data: {data}")
    
    # Load specific function
    dumps_func = loader.load_from_string('json.dumps')
    if dumps_func:
        result = dumps_func({'another': 'test'})
        print(f"Direct function result: {result}")

if __name__ == "__main__":
    example_usage()