from types import FunctionType, MethodType
from typing import final, override

from puripy.context.metadata import BeforedelMetadata, Metadata
from puripy.utils import MetadataUtils

from .decorator import functiondecorator
from .context_marker import ContextMarker


# noinspection PyPep8Naming
@final
@functiondecorator
class beforedel[T: FunctionType | MethodType](ContextMarker):

    @override
    def __call__(self, decoratable: T) -> T:
        metadata = self._to_metadata()
        MetadataUtils.append_metadata(decoratable, metadata)

        return decoratable

    @override
    def _to_metadata(self) -> Metadata:
        return BeforedelMetadata.instance()
