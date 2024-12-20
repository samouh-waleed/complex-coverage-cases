# tests/unit/core/test_meta_programming.py
import pytest
from src.core.meta_programming import singleton, debug_calls, MethodRegistryMetaclass

def test_singleton_decorator():
    @singleton
    class TestClass:
        def __init__(self):
            
            self.value = 0
            
    instance1 = TestClass()
    instance2 = TestClass()
    assert instance1 is instance2
    
    instance1.value = 42
    assert instance2.value == 42

def test_debug_calls(capsys):
    @debug_calls
    def test_function(x, y):
        return x + y
        
    result = test_function(2, 3)
    captured = capsys.readouterr()
    
    assert result == 5
    assert "Calling test_function" in captured.out
    assert "returned 5" in captured.out
