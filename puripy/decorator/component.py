import inspect
from typing import Callable, Any

from puripy.context import Context
from puripy.utility import ComponentUtility


def component[T](*args: Any, name: str = "") -> Callable[[type[T]], type[T]]:
    def wrapper(cls: Callable) -> type[T]:
        if ComponentUtility.has_string_annotations(cls):
            raise RuntimeError(f"Component {cls} has string-annotated dependencies. Is 'annotations' imported?")
        if ComponentUtility.has_empty_annotations(cls):
            raise RuntimeError(f"Component {cls} has unknown-type dependencies. Annotate all params.")

        if inspect.isabstract(cls):
            raise RuntimeError("Abstract class cannot be a component")

        context = Context()
        context.registrar.register_component(cls, name)

        return cls

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
