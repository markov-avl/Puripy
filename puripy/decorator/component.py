import inspect
from typing import Any

from typing_extensions import deprecated

from puripy.context import Context
from puripy.utility import ComponentUtility


@deprecated("Use puripy.context.annotation.Component instead")
def component[T](*args: type[T] | Any, name: str = "") -> type[T]:
    def wrapper(cls: type[T]) -> type[T]:
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
