from types import FunctionType, MethodType
from typing import final, override, Any

from puripy.context.decorator import DecoratableType
from puripy.context.metadata import DependsOnPropertyMetadata

from .marker import Marker


# noinspection PyPep8Naming
@final
class dependsonproperty[T: type | FunctionType | MethodType](Marker):

    def __init__(self, /, key: str, value: Any, match_on_missing: bool = False, path: str = ""):
        super().__init__([DecoratableType.CLASS, DecoratableType.FUNCTION, DecoratableType.METHOD])
        self.__key = key
        self.__value = value
        self.__match_on_missing = match_on_missing
        self.__path = path

    @override
    def _to_metadata(self) -> DependsOnPropertyMetadata:
        return DependsOnPropertyMetadata(
            key=self.__key,
            value=self.__value,
            match_on_missing=self.__match_on_missing,
            path=self.__path
        )
