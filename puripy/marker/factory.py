from typing import final, override

from puripy.context.decorator import DecoratableType
from puripy.context.metadata import FactoryMetadata

from .marker import Marker


# noinspection PyPep8Naming
@final
class factory[T: type](Marker):

    @override
    def __init__(self, /):
        super().__init__([DecoratableType.CLASS])

    @override
    def _to_metadata(self) -> FactoryMetadata:
        return FactoryMetadata.instance()
