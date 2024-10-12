from types import FunctionType, MethodType
from typing import final, override

from puripy.context.metadata import AfterinitMetadata, Metadata

from .decorator import functiondecorator
from .context_marker import ContextMarker


# noinspection PyPep8Naming
@final
@functiondecorator
class afterinit[T: FunctionType | MethodType](ContextMarker):

    @override
    def _to_metadata(self) -> Metadata:
        return AfterinitMetadata.instance()
