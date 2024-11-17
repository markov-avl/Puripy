from types import FunctionType
from typing import final, override

from puripy.context.decoration import DecoratableType
from puripy.context.metadata import BeforedelMetadata, Metadata

from .marker import Marker


# noinspection PyPep8Naming
@final
class beforedel[T: FunctionType](Marker):

    @override
    def __init__(self, /):
        super().__init__([DecoratableType.FUNCTION])

    @override
    def _to_metadata(self) -> Metadata:
        return BeforedelMetadata.instance()
