from collections.abc import Callable
from typing import Any

from typing_extensions import deprecated

from puripy.context.metadata import AfterinitMetadata
from puripy.utils import MetadataUtils


@deprecated("Use afterinit from puripy.context.marker instead")
def post_init[T](*args: Any) -> Callable[[type[T]], type[T]]:
    def wrapper(method: Callable) -> type[T]:
        metadata = AfterinitMetadata.instance()
        MetadataUtils.append_metadata(method, metadata)

        return method

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
