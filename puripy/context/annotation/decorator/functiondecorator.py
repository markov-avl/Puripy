from typing import Callable, final

from puripy.context.metadata import DecoratorMetadata
from puripy.utility import MetadataUtility


# noinspection PyPep8Naming
@final
class functiondecorator:
    """
    Adds metadata to make it clear that the decorator is for functions.
    """

    def __new__[C: Callable](cls, decoratable: C) -> C:
        metadata = DecoratorMetadata.of_function()
        MetadataUtility.append_metadata(decoratable, metadata)

        return decoratable
