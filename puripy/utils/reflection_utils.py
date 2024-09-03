import inspect
from typing import final, Callable


@final
class ReflectionUtils:

    @classmethod
    def is_method(cls, callable_: Callable) -> bool:
        return inspect.ismethod(callable_) or inspect.isfunction(callable_)

    @classmethod
    def params_of(cls, callable_: Callable) -> list[inspect.Parameter]:
        return list(inspect.signature(callable_).parameters.values())
