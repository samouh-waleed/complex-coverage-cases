from typing import List, Callable, Any, Dict
import operator
from functools import reduce

class LambdaUtils:
    """Utility class for working with lambda functions."""
    
    @staticmethod
    def create_sorter(key: str, reverse: bool = False) -> Callable:
        """Create a sorting function for dictionaries."""
        return lambda x: operator.itemgetter(key)(x)

    @staticmethod
    def create_filter(condition: Callable) -> Callable:
        """Create a filter function."""
        return lambda x: condition(x)

    @staticmethod
    def create_mapper(transform: Callable) -> Callable:
        """Create a mapping function."""
        return lambda x: transform(x)

    @staticmethod
    def chain_functions(functions: List[Callable]) -> Callable:
        """Chain multiple lambda functions together."""
        return lambda x: reduce(lambda acc, f: f(acc), functions, x)

    @staticmethod
    def create_validator(conditions: Dict[str, Callable]) -> Callable:
        """Create a validation function from multiple conditions."""
        return lambda x: all(
            func(operator.itemgetter(key)(x))
            for key, func in conditions.items()
        )