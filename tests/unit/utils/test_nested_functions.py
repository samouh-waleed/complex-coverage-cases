import pytest
from src.utils.nested_functions import create_counter, create_validator, memoize_with_ttl
import time

def test_counter_closure():
    counter = create_counter()
    
    assert counter('get') == 0
    assert counter('increment') == 1
    assert counter('increment', 2) == 3
    assert counter('decrement') == 2
    assert counter('get') == 2
    
    with pytest.raises(ValueError):
        counter('invalid_operation')

def test_validator_closure():
    rules = {
        'age': lambda x: isinstance(x, int) and x >= 0,
        'name': lambda x: isinstance(x, str) and len(x) > 0
    }
    
    validate = create_validator(rules)
    
    # Test valid data
    assert len(validate({'age': 25, 'name': 'John'})) == 0
    
    # Test invalid data
    errors = validate({'age': -1, 'name': ''})
    assert len(errors) == 2

def test_memoize_with_ttl():
    call_count = 0
    
    @memoize_with_ttl(ttl=1)  # 1 second TTL
    def expensive_function(x):
        nonlocal call_count
        call_count += 1
        return x * 2
    
    # First call
    assert expensive_function(5) == 10
    assert call_count == 1
    
    # Cached call
    assert expensive_function(5) == 10
    assert call_count == 1
    
    # Wait for TTL to expire
    time.sleep(1.1)
    
    # Should recalculate
    assert expensive_function(5) == 10
    assert call_count == 2
