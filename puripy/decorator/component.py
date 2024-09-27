import inspect
from typing import Any

from typing_extensions import deprecated

from puripy.context import Context
from puripy.context.metadata import ParticleMetadata
from puripy.utils import ParticleUtils, MetadataUtils


@deprecated("Use particle from puripy.context.marker instead")
def component[T](*args: type[T] | Any, name: str = "") -> type[T]:
    def wrapper(cls: type[T]) -> type[T]:
        metadata = ParticleMetadata(name)
        MetadataUtils.append_metadata(cls, metadata)

        if ParticleUtils.has_string_annotations(cls):
            raise RuntimeError(f"Component {cls} has string-annotated dependencies. Is 'annotations' imported?")
        if ParticleUtils.has_empty_annotations(cls):
            raise RuntimeError(f"Component {cls} has unknown-type dependencies. Annotate all params.")

        if inspect.isabstract(cls):
            raise RuntimeError("Abstract class cannot be a component")

        context = Context()
        context.registrar.register_particle(cls, name)

        return cls

    return wrapper(args[0]) if args and callable(args[0]) else wrapper
