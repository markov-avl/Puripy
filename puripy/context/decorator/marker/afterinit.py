from types import FunctionType
from typing import final, override

from puripy.context.decorator import DecoratableType
from puripy.context.metadata import AfterinitMetadata, Metadata

from .marker import Marker


# noinspection PyPep8Naming
@final
class afterinit[T: FunctionType](Marker):

    @override
    def __init__(self, /):
        super().__init__([DecoratableType.FUNCTION])

    @override
    def _to_metadata(self) -> Metadata:
        return AfterinitMetadata.instance()
