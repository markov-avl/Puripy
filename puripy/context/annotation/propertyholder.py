import inspect
import os
import re
from typing import Any, final

from pydantic import field_validator
from pydantic.dataclasses import dataclass

from puripy.context import Context

from .decorator import classdecorator, keywordsonly
from .contextannotation import ContextAnnotation


# noinspection PyPep8Naming
@final
@classdecorator
class propertyholder[T: type](ContextAnnotation):

    @keywordsonly
    def __init__(self, path: str = "", prefix: str = "", name: str = ""):
        super().__init__()
        self.__path = path
        self.__prefix = prefix
        self.__name = name

    def __call__(self, decoratable: T) -> T:
        context = Context()
        context.registrar.register_property_holder(decoratable, self.__path, self.__prefix, self.__name)

        self.__make_inner_fields_extractable_recursively(decoratable)
        self.__make_inner_classes_as_dataclasses_recursively(decoratable)

        # noinspection PyTypeChecker
        return dataclass(decoratable)

    def __make_inner_fields_extractable_recursively(self, decoratable: T) -> None:
        # noinspection PyUnresolvedReferences
        extractor = field_validator(*decoratable.__annotations__.keys(), mode="before")
        decoratable.__extract__ = extractor(self.__extract_env)
        for attr, value in decoratable.__dict__.items():
            if inspect.isclass(value):
                self.__make_inner_fields_extractable_recursively(value)

    def __make_inner_classes_as_dataclasses_recursively(self, decoratable: T) -> None:
        for attr, value in decoratable.__dict__.items():
            if inspect.isclass(value):
                self.__make_inner_classes_as_dataclasses_recursively(value)
                # noinspection PyTypeChecker
                setattr(decoratable, attr, dataclass(value))

    @staticmethod
    def __extract_env(value: Any) -> Any:
        if isinstance(value, str):
            for match in re.finditer(r'\$\{([A-Za-z0-9_-]+)(:([^}]*))?}', value):
                env = os.getenv(match.group(1))
                if env is None:
                    if match.group(2) is None:
                        raise RuntimeError(f"Environment '{match.group(1)}' cannot be resolved")
                    env = match.group(3)
                value = value.replace(match.group(0), env)
        return value
