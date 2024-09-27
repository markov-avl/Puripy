from typing import Any, Callable

from typing_extensions import deprecated

from puripy.context.metadata import BeforedelMetadata
from puripy.utils import MetadataUtils


@deprecated("Use beforedel from puripy.context.marker instead")
def pre_del[T](*args: Any) -> Callable[[type[T]], type[T]]:
    def wrapper(method: Callable) -> type[T]:
        metadata = BeforedelMetadata.instance()
        MetadataUtils.append_metadata(method, metadata)

        return method

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
