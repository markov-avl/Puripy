import inspect
from typing import final, Callable


@final
class ReflectionUtils:

    @classmethod
    def is_method_or_function(cls, callable_: Callable) -> bool:
        return inspect.ismethod(callable_) or inspect.isfunction(callable_)

    @classmethod
    def is_defined_in_any(cls, obj: object, packages: set[str]) -> bool:
        for package in packages:
            if obj.__module__.startswith(package):
                return True
        return False

    @classmethod
    def params_of(cls, callable_: Callable) -> list[inspect.Parameter]:
        return list(inspect.signature(callable_).parameters.values())
