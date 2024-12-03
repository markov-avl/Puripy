import inspect
from collections.abc import Callable

from puripy.context.decorator import DecoratableType

__DECORATABLE_VALIDATORS = {
    DecoratableType.CLASS: inspect.isclass,
    DecoratableType.FUNCTION: inspect.isfunction,
    DecoratableType.METHOD: inspect.ismethod
}


def is_valid_decoratable(decoratable: Callable, valid_types: list[DecoratableType]) -> bool:
    return any(v(decoratable) for t, v in __DECORATABLE_VALIDATORS.items() if t in valid_types)
