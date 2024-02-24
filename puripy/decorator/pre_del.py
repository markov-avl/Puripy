from typing import Any, Callable

from decohints import decohints


@decohints
def pre_del[T](*args: Any) -> Callable[[type[T]], type[T]]:
    def wrapper(method: Callable) -> type[T]:
        method.__pre_del__ = True

        return method

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
