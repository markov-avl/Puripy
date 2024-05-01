import inspect
import os
import re
from typing import Any

from pydantic import field_validator
from pydantic.dataclasses import dataclass

from puripy.context import Context

from .decorator import ClassDecorator, KeywordsOnly
from .context_annotation import ContextAnnotation


@ClassDecorator
class PropertyHolder[Callable](ContextAnnotation):

    @KeywordsOnly
    def __init__(self, path: str = "", prefix: str = "", name: str = ""):
        super().__init__()
        self._path = path
        self._prefix = prefix
        self._name = name

    def __call__(self, decoratable):
        context = Context()
        context.registrar.register_property_holder(decoratable, self._path, self._prefix, self._name)

        self._make_inner_fields_extractable_recursively(decoratable)
        self._make_inner_classes_as_dataclasses_recursively(decoratable)

        # noinspection PyTypeChecker
        return dataclass(decoratable)

    def _make_inner_fields_extractable_recursively(self, decoratable: Callable):
        # noinspection PyUnresolvedReferences
        decoratable.__extract__ = field_validator(*decoratable.__annotations__.keys(), mode='before')(self._extract_env)
        for attr, value in decoratable.__dict__.items():
            if inspect.isclass(value):
                self._make_inner_fields_extractable_recursively(value)

    def _make_inner_classes_as_dataclasses_recursively(self, decoratable: Callable) -> None:
        for attr, value in decoratable.__dict__.items():
            if inspect.isclass(value):
                self._make_inner_classes_as_dataclasses_recursively(value)
                # noinspection PyTypeChecker
                setattr(decoratable, attr, dataclass(value))

    @staticmethod
    def _extract_env(value: Any) -> Any:
        if isinstance(value, str):
            for match in re.finditer(r'\$\{([A-Za-z0-9_-]+)(:([^}]*))?}', value):
                env = os.getenv(match.group(1))
                if env is None:
                    if match.group(2) is None:
                        raise RuntimeError(f"Environment '{match.group(1)}' cannot be resolved")
                    env = match.group(3)
                value = value.replace(match.group(0), env)
        return value
