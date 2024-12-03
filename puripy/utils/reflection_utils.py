import inspect
from collections.abc import Callable
from typing import Any


def params_of(obj: Callable) -> list[inspect.Parameter]:
    return list(inspect.signature(obj).parameters.values())


def return_type_of(obj: Callable) -> Any:
    return obj if inspect.isclass(obj) else inspect.signature(obj).return_annotation


def defined_name(obj: Any) -> str:
    if inspect.isclass(obj):
        return obj.__name__
    if inspect.isfunction(obj):  # or inspect.ismethod(obj):
        return obj.__qualname__.split(".")[-1]
    return obj.__class__.__name__


def has_incorrect_annotations(obj: Callable) -> bool:
    return has_string_annotations(obj) or has_empty_annotations(obj)


def has_string_annotations(obj: Callable) -> bool:
    return any(isinstance(param.annotation, str) for param in params_of(obj))


def has_empty_annotations(obj: Callable) -> bool:
    return any(param.annotation is inspect.Parameter.empty for param in params_of(obj))
