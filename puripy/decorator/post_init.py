from typing import Any, Callable

from typing_extensions import deprecated


@deprecated("Use puripy.context.annotation.postinit instead")
def post_init[T](*args: Any) -> Callable[[type[T]], type[T]]:
    def wrapper(method: Callable) -> type[T]:
        method.__post_init__ = 934

        return method

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
