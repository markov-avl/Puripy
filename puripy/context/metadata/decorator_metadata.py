from __future__ import annotations

from enum import StrEnum

from .metadata import Metadata


class DecoratorMetadata(Metadata):
    class DecoratableType(StrEnum):
        CLASS = "class"
        FUNCTION = "function"

    __CLASS_INSTANCE = None
    __FUNCTION_INSTANCE = None

    def __init__(self, decoratable_type: DecoratableType):
        self.__decoratable_type = decoratable_type

    def for_classes(self) -> bool:
        return self.__decoratable_type == self.DecoratableType.CLASS

    def for_functions(self) -> bool:
        return self.__decoratable_type == self.DecoratableType.FUNCTION

    @classmethod
    def of_class(cls) -> DecoratorMetadata:
        if cls.__CLASS_INSTANCE is None:
            cls.__CLASS_INSTANCE = cls(cls.DecoratableType.CLASS)
        return cls.__CLASS_INSTANCE

    @classmethod
    def of_function(cls) -> DecoratorMetadata:
        if cls.__FUNCTION_INSTANCE is None:
            cls.__FUNCTION_INSTANCE = cls(cls.DecoratableType.FUNCTION)
        return cls.__FUNCTION_INSTANCE
