import pytest
from src.core.dynamic_imports import DynamicImporter, ModuleRegistry

def test_dynamic_module_import():
    importer = DynamicImporter()
    # Test standard library import
    json_module = importer.import_module('json')
    assert json_module is not None
    
    # Test non-existent module
    invalid_module = importer.import_module('non_existent_module')
    assert invalid_module is None

def test_import_from_string():
    # Test importing specific object from module
    obj = DynamicImporter.import_from_string('json.dumps')
    assert callable(obj)
    
    with pytest.raises(ImportError):
        DynamicImporter.import_from_string('invalid.module.path')

@pytest.mark.asyncio
async def test_lazy_import_decorator():
    @DynamicImporter.lazy_import('json')
    def process_json(data):
        return process_json.module.dumps(data)
    
    result = process_json({"test": "data"})
    assert isinstance(result, str)
    assert "test" in result

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
