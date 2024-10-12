from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

from puripy.context.metadata import Metadata
from puripy.utils import ValidationUtils, MetadataUtils


class ContextMarker[C: Callable](ABC):

    def __new__(cls, *args, **kwargs) -> ContextMarker | C:
        marker = super().__new__(cls)
        marker.__init__(**kwargs)

        if args and callable(args[0]):
            ValidationUtils.validate_decoratable(marker, args[0])
            return marker(args[0])

        return marker

    def __init__(self, /, **kwargs):
        pass

    def __call__(self, decoratable: C) -> C:
        metadata = self._to_metadata()
        MetadataUtils.append_metadata(decoratable, metadata)

        return decoratable

    @abstractmethod
    def _to_metadata(self) -> Metadata: ...
