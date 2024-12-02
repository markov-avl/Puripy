import inspect
from collections.abc import Callable


def is_defined_in_any(module_name: str, packages: set[str]) -> bool:
    return any(module_name.startswith(package) for package in packages)


def params_of(callable_: Callable) -> list[inspect.Parameter]:
    return list(inspect.signature(callable_).parameters.values())
