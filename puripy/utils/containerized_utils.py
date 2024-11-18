import inspect
from collections.abc import Callable
from typing import Any

import inflection

from .reflection_utils import params_of


def get_name(obj: Any, name: str = "") -> str:
    if name:
        return name
    return inflection.underscore(obj.__name__ if inspect.isclass(obj) else obj.__class__.__name__)


def has_incorrect_annotations(obj: Callable) -> bool:
    return has_string_annotations(obj) or has_empty_annotations(obj)


def has_string_annotations(obj: Callable) -> bool:
    return any(isinstance(param.annotation, str) for param in params_of(obj))


def has_empty_annotations(obj: Callable) -> bool:
    return any(issubclass(param.annotation, inspect.Parameter.empty) for param in params_of(obj))
