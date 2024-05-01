from __future__ import annotations

from enum import StrEnum

from .metadata import Metadata


class DecoratorMetadata(Metadata):
    class DecoratableType(StrEnum):
        CLASS = "class"
        FUNCTION = "function"

    def __init__(self, decoratable_type: DecoratableType):
        self._decoratable_type = decoratable_type

    def for_classes(self) -> bool:
        return self._decoratable_type == self.DecoratableType.CLASS

    def for_functions(self) -> bool:
        return self._decoratable_type == self.DecoratableType.FUNCTION

    @classmethod
    def of_class(cls) -> DecoratorMetadata:
        return DecoratorMetadata(cls.DecoratableType.CLASS)

    @classmethod
    def of_function(cls) -> DecoratorMetadata:
        return DecoratorMetadata(cls.DecoratableType.FUNCTION)
