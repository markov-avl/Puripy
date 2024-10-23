from collections.abc import Callable
from typing import final

from puripy.context.metadata import DecoratorMetadata
from puripy.utils.metadata_utils import append_metadata


# noinspection PyPep8Naming
@final
class functiondecorator:
    """
    Adds metadata to make it clear that the decorator is for functions.
    """

    def __new__[C: Callable](cls, decoratable: C) -> C:
        metadata = DecoratorMetadata.of_function()
        append_metadata(decoratable, metadata)

        return decoratable
