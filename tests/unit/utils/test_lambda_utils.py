import pytest
from src.utils.lambda_utils import LambdaUtils

def test_create_sorter():
    data = [
        {'name': 'John', 'age': 30},
        {'name': 'Alice', 'age': 25}
    ]
    
    # Sort by name
    name_sorter = LambdaUtils.create_sorter('name')
    sorted_data = sorted(data, key=name_sorter)
    assert sorted_data[0]['name'] == 'Alice'
    
    # Sort by age
    age_sorter = LambdaUtils.create_sorter('age')
    sorted_data = sorted(data, key=age_sorter)
    assert sorted_data[0]['age'] == 25

def test_create_filter():
    numbers = [1, 2, 3, 4, 5]
    
    is_even = LambdaUtils.create_filter(lambda x: x % 2 == 0)
    even_numbers = list(filter(is_even, numbers))
    
    assert even_numbers == [2, 4]

def test_create_mapper():
    numbers = [1, 2, 3]
    
    double = LambdaUtils.create_mapper(lambda x: x * 2)
    doubled = list(map(double, numbers))
    
    assert doubled == [2, 4, 6]

def test_chain_functions():
    functions = [
        lambda x: x * 2,    # double
        lambda x: x + 1,    # add one
        lambda x: x ** 2    # square
    ]
    
    chained = LambdaUtils.chain_functions(functions)
    
    # ((2 * 2) + 1)^2 = 25
    assert chained(2) == 25

def test_create_validator():
    conditions = {
        'age': lambda x: x >= 18,
        'name': lambda x: len(x) > 0
    }
    
    validator = LambdaUtils.create_validator(conditions)
    
    valid_data = {'age': 20, 'name': 'John'}
    invalid_data = {'age': 16, 'name': ''}
    
    assert validator(valid_data) is True
    assert validator(invalid_data) is False