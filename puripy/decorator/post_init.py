from typing import Any, Callable

from typing_extensions import deprecated


@deprecated("Use afterinit from puripy.context.marker instead")
def post_init[T](*args: Any) -> Callable[[type[T]], type[T]]:
    def wrapper(method: Callable) -> type[T]:
        method.__afterinit__ = True

        return method

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
