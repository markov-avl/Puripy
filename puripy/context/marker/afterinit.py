from types import FunctionType, MethodType
from typing import final

from puripy.context.metadata import AfterinitMetadata, Metadata
from puripy.utils import MetadataUtils

from .decorator import functiondecorator
from .context_marker import ContextMarker


# noinspection PyPep8Naming
@final
@functiondecorator
class afterinit[T: FunctionType | MethodType](ContextMarker):

    def __call__(self, decoratable: T) -> T:
        metadata = self._to_metadata()
        MetadataUtils.append_metadata(decoratable, metadata)

        return decoratable

    def _to_metadata(self) -> Metadata:
        return AfterinitMetadata.instance()
