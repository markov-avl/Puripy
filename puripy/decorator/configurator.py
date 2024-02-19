from typing import Callable, Any


def configurator[T](*args: Any) -> Callable[[type[T]], type[T]]:
    def wrapper(cls: Callable) -> type[T]:
        return cls

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
