from collections.abc import Iterable
from typing import final, override

from puripy.context.decorator import DecoratableType
from puripy.context.metadata import ScanPackagesMetadata

from .marker import Marker


# noinspection PyPep8Naming
@final
class scanpackages[T: type](Marker):

    def __init__(self, /, include: str | Iterable[str] = None, exclude: str | Iterable[str] = None):
        super().__init__([DecoratableType.CLASS])
        self.__include = self.__to_set(include)
        self.__exclude = self.__to_set(exclude)

    @override
    def _to_metadata(self) -> ScanPackagesMetadata:
        return ScanPackagesMetadata(include=self.__include, exclude=self.__exclude)

    @staticmethod
    def __to_set(value) -> set[str]:
        if value is None:
            return set()
        if isinstance(value, str):
            return {value}
        if isinstance(value, Iterable):
            return set(value)
        raise TypeError("Expected a string, an iterable of strings, or None")
