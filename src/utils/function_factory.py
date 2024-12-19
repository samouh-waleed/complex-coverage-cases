from functools import wraps
from typing import Callable, Dict, Any, List, Optional
import inspect

class FunctionFactory:
    """Factory for creating functions dynamically."""
    
    @staticmethod
    def create_math_function(operation: str) -> Callable:
        """Create basic math functions."""
        def add(a: float, b: float) -> float:
            return a + b
            
        def subtract(a: float, b: float) -> float:
            return a - b
            
        def multiply(a: float, b: float) -> float:
            return a * b
            
        def divide(a: float, b: float) -> float:
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
            
        operations = {
            'add': add,
            'subtract': subtract,
            'multiply': multiply,
            'divide': divide
        }
        
        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")
            
        return operations[operation]

    @staticmethod
    def create_composite_function(functions: List[Callable]) -> Callable:
        """Create a function that composes multiple functions."""
        def composite(*args, **kwargs):
            result = functions[0](*args, **kwargs)
            for func in functions[1:]:
                result = func(result)
            return result
        return composite

    @classmethod
    def create_method_with_hooks(
        cls,
        main_func: Callable,
        before_hooks: Optional[List[Callable]] = None,
        after_hooks: Optional[List[Callable]] = None
    ) -> Callable:
        """Create a method with before and after hooks."""
        before_hooks = before_hooks or []
        after_hooks = after_hooks or []
        
        @wraps(main_func)
        def method(*args, **kwargs):
            # Execute before hooks
            for hook in before_hooks:
                hook(*args, **kwargs)
                
            # Execute main function
            result = main_func(*args, **kwargs)
            
            # Execute after hooks
            for hook in after_hooks:
                hook(result, *args, **kwargs)
                
            return result
            
        return method