from typing import Any, Callable


def post_init[T](*args: Any) -> Callable[[type[T]], type[T]]:
    def wrapper(method: Callable) -> type[T]:
        method.__post_init__ = True

        return method

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
