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