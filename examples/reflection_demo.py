"""Example of Python reflection and introspection capabilities."""
import inspect
from typing import Any, Callable, Dict, List, Type
from dataclasses import dataclass

@dataclass
class ExampleData:
    """Example dataclass for reflection."""
    name: str
    value: int

class ReflectionDemo:
    """Demonstrates various reflection capabilities."""
    
    @staticmethod
    def get_class_info(cls: Type) -> Dict[str, Any]:
        """Get information about a class using reflection."""
        return {
            'name': cls.__name__,
            'bases': [base.__name__ for base in cls.__bases__],
            'methods': [
                name for name, _ in inspect.getmembers(cls, predicate=inspect.isfunction)
            ],
            'attributes': [
                name for name, _ in inspect.getmembers(cls, lambda x: not inspect.isroutine(x))
            ]
        }
    
    @staticmethod
    def get_function_info(func: Callable) -> Dict[str, Any]:
        """Get information about a function using reflection."""
        sig = inspect.signature(func)
        return {
            'name': func.__name__,
            'parameters': list(sig.parameters.keys()),
            'annotations': {
                name: param.annotation.__name__ 
                if hasattr(param.annotation, '__name__') else str(param.annotation)
                for name, param in sig.parameters.items()
            },
            'docstring': inspect.getdoc(func)
        }
    
    @classmethod
    def create_dynamic_class(
        cls,
        class_name: str,
        attributes: Dict[str, Any],
        methods: Dict[str, Callable]
    ) -> Type:
        """Create a new class dynamically."""
        return type(class_name, (object,), {**attributes, **methods})

def example_function(x: int, y: str = "default") -> List[Any]:
    """Example function for reflection."""
    return [x, y]

def example_usage():
    """Example usage of reflection capabilities."""
    demo = ReflectionDemo()
    
    # Class reflection
    class_info = demo.get_class_info(ExampleData)
    print("Class Info:", class_info)
    
    # Function reflection
    func_info = demo.get_function_info(example_function)
    print("Function Info:", func_info)
    
    # Dynamic class creation
    attributes = {'x': 1, 'y': 2}
    methods = {
        'get_sum': lambda self: self.x + self.y,
        'get_product': lambda self: self.x * self.y
    }
    
    DynamicClass = demo.create_dynamic_class('DynamicClass', attributes, methods)
    instance = DynamicClass()
    print(f"Sum: {instance.get_sum()}")
    print(f"Product: {instance.get_product()}")

if __name__ == "__main__":
    example_usage()