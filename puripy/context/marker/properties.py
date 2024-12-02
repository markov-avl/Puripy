import inspect
import os
import re
from typing import Any, final, override

from pydantic import field_validator
from pydantic.dataclasses import dataclass

from puripy.context.decoration import DecoratableType
from puripy.context.metadata import PropertiesMetadata, Metadata

from .marker import Marker


# noinspection PyPep8Naming
@final
class properties[T: type](Marker):

    def __init__(self, /, path: str = "", prefix: str = "", name: str = ""):
        super().__init__([DecoratableType.CLASS])
        self.__path = path
        self.__prefix = prefix
        self.__name = name

    @override
    def __call__(self, decoratable: T) -> T:
        self.__make_inner_fields_extractable_recursively(decoratable)
        self.__make_inner_classes_as_dataclasses_recursively(decoratable)

        # noinspection PyTypeChecker
        return super().__call__(dataclass(decoratable))

    @override
    def _to_metadata(self) -> Metadata:
        return PropertiesMetadata(name=self.__name, prefix=self.__prefix, path=self.__path)

    def __make_inner_fields_extractable_recursively(self, decoratable: T) -> None:
        # noinspection PyUnresolvedReferences
        extractor = field_validator(*decoratable.__annotations__.keys(), mode="before")
        decoratable.__extract__ = extractor(self.__extract_env)
        for value in decoratable.__dict__.values():
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
            for match in re.finditer(r"\$\{([A-Za-z0-9_-]+)(:([^}]*))?}", value):
                if (env := os.getenv(match.group(1))) is None:
                    if match.group(2) is None:
                        raise RuntimeError(f"Environment '{match.group(1)}' cannot be resolved")
                    env = match.group(3)
                value = value.replace(match.group(0), env)
        return value
