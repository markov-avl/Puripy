import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import final, Any

from puripy.utils import MetadataUtils


@final
class ValidationUtils:
    @dataclass
    class DecoratableValidation:
        type: str
        validator: Callable[[Any], bool]
        validate: bool

    @classmethod
    def validate_decoratable(cls, marker: Any, decoratable: Callable) -> None:
        decoratable_validations = (
            cls.DecoratableValidation("class", inspect.isclass, MetadataUtils.is_class_decorator(marker)),
            cls.DecoratableValidation("function", inspect.isfunction, MetadataUtils.is_function_decorator(marker))
        )

        if not any(v.validator(decoratable) for v in decoratable_validations if v.validate):
            valid_types = ", ".join(v.type for v in decoratable_validations if v.validate)
            raise RuntimeError(f"Decorated object {decoratable} must be any of the following types: {valid_types}")
