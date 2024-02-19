import inspect
from inspect import _empty
from typing import final, Any, Callable

import inflection

from .reflection_utility import ReflectionUtility


@final
class ComponentUtility:

    @staticmethod
    def get_name(obj: Any, name: str = "") -> str:
        obj_name = obj.__name__ if inspect.isclass(obj) else obj.__class__.__name__
        return name if name else inflection.underscore(obj_name)

    @staticmethod
    def has_incorrect_annotations(obj: Callable) -> bool:
        return ComponentUtility.has_string_annotations(obj) or ComponentUtility.has_empty_annotations(obj)

    @staticmethod
    def has_string_annotations(obj: Callable) -> bool:
        return any(isinstance(param.annotation, str) for param in ReflectionUtility.params_of(obj))

    @staticmethod
    def has_empty_annotations(obj: Callable) -> bool:
        return any(issubclass(param.annotation, _empty) for param in ReflectionUtility.params_of(obj))
