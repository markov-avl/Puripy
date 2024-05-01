import inspect
from dataclasses import dataclass
from typing import final, Any, Callable

from puripy.utility import MetadataUtility


@dataclass
class _DecoratableValidation:
    type: str
    validator: Callable[[Any], bool]
    validate: bool


@final
class ValidationUtility:

    @classmethod
    def validate_decoratable(cls, annotation: Any, decoratable: Callable) -> None:
        decoratable_validations = [
            _DecoratableValidation("class", inspect.isclass, MetadataUtility.is_class_decorator(annotation)),
            _DecoratableValidation("function", inspect.isfunction, MetadataUtility.is_function_decorator(annotation))
        ]

        if not any(v.validator(decoratable) for v in decoratable_validations if v.validate):
            valid_types = ", ".join(v.type for v in decoratable_validations if v.validate)
            raise RuntimeError(f"Decorated object {decoratable} must be any of the following types: {valid_types}")
