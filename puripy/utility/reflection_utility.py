import inspect
from typing import final, Callable


@final
class ReflectionUtility:

    @staticmethod
    def is_method(callable_: Callable) -> bool:
        return inspect.ismethod(callable_) or inspect.isfunction(callable_)

    @staticmethod
    def params_of(callable_: Callable) -> list[inspect.Parameter]:
        return list(inspect.signature(callable_).parameters.values())
