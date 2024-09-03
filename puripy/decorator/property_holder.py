import inspect
import os
import re
from typing import Callable, Any

from pydantic import field_validator
from pydantic.dataclasses import dataclass
from typing_extensions import deprecated

from puripy.context import Context


@deprecated("Use puripy.context.annotation.properties instead")
def property_holder[T](*args: Any, path: str = "", prefix: str = "", name: str = "") -> Callable[[type[T]], type[T]]:
    def wrapper(cls: Callable) -> type[T]:
        context = Context()
        context.registrar.register_properties(cls, path, prefix, name)

        _make_inner_fields_extractable_recursively(cls)
        _make_inner_classes_as_dataclasses_recursively(cls)

        return dataclass(cls)

    return wrapper(args[0]) if args and callable(args[0]) else wrapper


def _extract_env(value: Any):
    if isinstance(value, str):
        for match in re.finditer(r'\$\{([A-Za-z0-9_-]+)(:([^}]*))?}', value):
            env = os.getenv(match.group(1))
            if env is None:
                if match.group(2) is None:
                    raise RuntimeError(f"Environment '{match.group(1)}' cannot be resolved")
                env = match.group(3)
            value = value.replace(match.group(0), env)
    return value


def _make_inner_fields_extractable_recursively(cls: Callable):
    # noinspection PyUnresolvedReferences
    cls.__extract__ = field_validator(*cls.__annotations__.keys(), mode='before')(_extract_env)
    for attr, value in cls.__dict__.items():
        if inspect.isclass(value):
            _make_inner_fields_extractable_recursively(value)


def _make_inner_classes_as_dataclasses_recursively(cls: Callable) -> None:
    for attr, value in cls.__dict__.items():
        if inspect.isclass(value):
            _make_inner_classes_as_dataclasses_recursively(value)
            # noinspection PyTypeChecker
            setattr(cls, attr, dataclass(value))
