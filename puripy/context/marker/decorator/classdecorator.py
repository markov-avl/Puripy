from typing import Callable, final

from puripy.context.metadata import DecoratorMetadata
from puripy.utils import MetadataUtils


# noinspection PyPep8Naming
@final
class classdecorator:
    """
    Adds metadata to make it clear that the decorator is for classes.
    """

    def __new__[C: Callable](cls, decoratable: C) -> C:
        metadata = DecoratorMetadata.of_class()
        MetadataUtils.append_metadata(decoratable, metadata)

        return decoratable
