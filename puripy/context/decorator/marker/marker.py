from __future__ import annotations

from abc import abstractmethod, ABC
from collections.abc import Callable

from puripy.context.decorator import DecoratableType
from puripy.context.metadata import Metadata
from puripy.utils.metadata_utils import append_metadata
from puripy.utils.validation_utils import is_valid_decoratable


class Marker[C: Callable](ABC):

    def __new__(cls, *args, **kwargs) -> Marker | C:
        marker = super().__new__(cls)
        marker.__init__(**kwargs)

        return marker(args[0]) if args and callable(args[0]) else marker

    def __init__(self, valid_types: list[DecoratableType]):
        self.__valid_types = valid_types

    def __call__(self, decoratable: C) -> C:
        self.__validate_decoratable(decoratable)
        self.__append_metadata(decoratable)

        return decoratable

    def __validate_decoratable(self, decoratable: Callable) -> None:
        if not is_valid_decoratable(decoratable, self.__valid_types):
            valid_types = ", ".join(self.__valid_types)
            raise RuntimeError(f"Decorated object {decoratable} must be any of the following types: {valid_types}")

    def __append_metadata(self, decoratable: Callable) -> None:
        metadata = self._to_metadata()
        append_metadata(decoratable, metadata)

    @abstractmethod
    def _to_metadata(self) -> Metadata: ...
