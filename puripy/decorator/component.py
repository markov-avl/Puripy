import inspect
from typing import Any

from typing_extensions import deprecated

from puripy.context import Context
from puripy.utils import ComponentUtils


@deprecated("Use puripy.context.annotation.component instead")
def component[T](*args: type[T] | Any, name: str = "") -> type[T]:
    def wrapper(cls: type[T]) -> type[T]:
        if ComponentUtils.has_string_annotations(cls):
            raise RuntimeError(f"Component {cls} has string-annotated dependencies. Is 'annotations' imported?")
        if ComponentUtils.has_empty_annotations(cls):
            raise RuntimeError(f"Component {cls} has unknown-type dependencies. Annotate all params.")

        if inspect.isabstract(cls):
            raise RuntimeError("Abstract class cannot be a component")

        context = Context()
        context.registrar.register_component(cls, name)

        return cls

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
