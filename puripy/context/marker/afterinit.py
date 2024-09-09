from types import FunctionType
from typing import final

from puripy.context.metadata import AfterinitMetadata
from puripy.utils import MetadataUtils

from .decorator import functiondecorator
from .context_marker import ContextMarker


# noinspection PyPep8Naming
@final
@functiondecorator
class afterinit[F: FunctionType](ContextMarker):

    def __call__(self, decoratable: F) -> F:
        metadata = AfterinitMetadata.instance()
        MetadataUtils.append_metadata(decoratable, metadata)

        return decoratable