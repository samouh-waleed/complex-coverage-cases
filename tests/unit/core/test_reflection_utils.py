import pytest
from src.core.reflection_utils import ReflectionUtils

def test_get_methods():
    class TestClass:
        def public_method(self): pass
        def _private_method(self): pass
        
    methods = ReflectionUtils.get_methods(TestClass)
    assert 'public_method' in methods
    assert '_private_method' not in methods

def test_create_dynamic_class():
    # Create a class with attributes and methods
    attributes = {'value': 42}
    methods = {
        'get_value': lambda self: self.value,
        'set_value': lambda self, x: setattr(self, 'value', x)
    }
    
    DynamicClass = ReflectionUtils.create_dynamic_class(
        'DynamicClass',
        attributes,
        methods
    )
    
    instance = DynamicClass()
    assert instance.value == 42
    instance.set_value(100)
    assert instance.get_value() == 100