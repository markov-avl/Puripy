import inspect
from collections.abc import Callable
from typing import final


@final
class ReflectionUtils:

    @classmethod
    def is_method_or_function(cls, callable_: Callable) -> bool:
        return inspect.ismethod(callable_) or inspect.isfunction(callable_)

    @classmethod
    def is_defined_in_any(cls, module_name: str, packages: set[str]) -> bool:
        return any(module_name.startswith(package) for package in packages)

    @classmethod
    def params_of(cls, callable_: Callable) -> list[inspect.Parameter]:
        return list(inspect.signature(callable_).parameters.values())
