import pytest
from src.utils.function_factory import FunctionFactory

def test_create_math_function():
    add_func = FunctionFactory.create_math_function('add')
    assert add_func(2, 3) == 5
    
    divide_func = FunctionFactory.create_math_function('divide')
    assert divide_func(6, 2) == 3
    
    with pytest.raises(ValueError):
        divide_func(1, 0)
    
    with pytest.raises(ValueError):
        FunctionFactory.create_math_function('invalid_op')

def test_create_composite_function():
    def double(x): return x * 2
    def add_one(x): return x + 1
    def square(x): return x * x
    
    composite = FunctionFactory.create_composite_function([
        double,
        add_one,
        square
    ])
    
    # (2 * 2 + 1)^2 = 25
    assert composite(2) == 25

def test_create_method_with_hooks():
    calls = []
    
    def before_hook(*args, **kwargs):
        calls.append('before')
    
    def after_hook(result, *args, **kwargs):
        calls.append('after')
    
    def main_func(x):
        calls.append('main')
        return x * 2
    
    method = FunctionFactory.create_method_with_hooks(
        main_func,
        [before_hook],
        [after_hook]
    )
    
    result = method(5)
    
    assert result == 10
    assert calls == ['before', 'main', 'after']