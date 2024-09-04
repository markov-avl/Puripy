from types import FunctionType
from typing import final

from puripy.context.metadata import BeforedelMetadata
from puripy.utils import MetadataUtils

from .decorator import functiondecorator
from .context_annotation import ContextAnnotation


# noinspection PyPep8Naming
@final
@functiondecorator
class beforedel[F: FunctionType](ContextAnnotation):

    def __call__(self, decoratable: F) -> F:
        metadata = BeforedelMetadata.instance()
        MetadataUtils.append_metadata(decoratable, metadata)

        return decoratable
