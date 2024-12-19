from typing import Callable, List, Dict, Any, Optional
from functools import wraps
import time

def create_counter() -> Callable:
    """Create a counter with closure."""
    count = 0
    
    def increment(amount: int = 1) -> int:
        nonlocal count
        count += amount
        return count
        
    def decrement(amount: int = 1) -> int:
        nonlocal count
        count -= amount
        return count
    
    def get_count() -> int:
        return count
    
    # Create a function that contains other functions
    def counter_ops(operation: str, amount: int = 1) -> int:
        if operation == 'increment':
            return increment(amount)
        elif operation == 'decrement':
            return decrement(amount)
        elif operation == 'get':
            return get_count()
        raise ValueError(f"Unknown operation: {operation}")
        
    return counter_ops

def create_validator(rules: Dict[str, Callable]) -> Callable:
    """Create a validator with custom rules."""
    def validate(data: Dict[str, Any]) -> List[str]:
        errors = []
        
        def check_rule(key: str, rule: Callable):
            try:
                if not rule(data.get(key)):
                    errors.append(f"Validation failed for {key}")
            except Exception as e:
                errors.append(f"Error validating {key}: {str(e)}")
        
        for key, rule in rules.items():
            check_rule(key, rule)
            
        return errors
        
    return validate

def memoize_with_ttl(ttl: int = 60):
    """Create a memoization decorator with TTL."""
    cache: Dict[str, Dict[str, Any]] = {}
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(kwargs)
            
            # Check if result exists and is still valid
            if key in cache:
                result, timestamp = cache[key]['result'], cache[key]['timestamp']
                if time.time() - timestamp < ttl:
                    return result
                    
            # Calculate new result
            result = func(*args, **kwargs)
            cache[key] = {
                'result': result,
                'timestamp': time.time()
            }
            
            return result
        return wrapper
    return decorator
