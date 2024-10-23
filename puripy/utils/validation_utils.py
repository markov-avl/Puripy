import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .metadata_utils import is_class_decorator, is_function_decorator


@dataclass
class DecoratableValidation:
    type: str
    validator: Callable[[Any], bool]
    validate: bool


def validate_decoratable(marker: Any, decoratable: Callable) -> None:
    decoratable_validations = (
        DecoratableValidation("class", inspect.isclass, is_class_decorator(marker)),
        DecoratableValidation("function", inspect.isfunction, is_function_decorator(marker))
    )

    if not any(v.validator(decoratable) for v in decoratable_validations if v.validate):
        valid_types = ", ".join(v.type for v in decoratable_validations if v.validate)
        raise RuntimeError(f"Decorated object {decoratable} must be any of the following types: {valid_types}")
