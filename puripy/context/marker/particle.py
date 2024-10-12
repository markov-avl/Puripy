import inspect
from typing import final, override

from puripy.context.metadata import ParticleMetadata, Metadata
from puripy.utils import ContainerizedUtils

from .decorator import classdecorator
from .context_marker import ContextMarker


# noinspection PyPep8Naming
@final
@classdecorator
class particle[T: type](ContextMarker):

    def __init__(self, /, name: str = ""):
        super().__init__()
        self.__name = name

    @override
    def __call__(self, decoratable: T) -> T:
        if ContainerizedUtils.has_string_annotations(decoratable):
            raise RuntimeError(f"Particle {decoratable} has string-annotated dependencies. Is 'annotations' imported?")
        if ContainerizedUtils.has_empty_annotations(decoratable):
            raise RuntimeError(f"Particle {decoratable} has unknown-type dependencies. Annotate all params.")

        if inspect.isabstract(decoratable):
            raise RuntimeError("Abstract class cannot be a particle")

        return super().__call__(decoratable)

    @override
    def _to_metadata(self) -> Metadata:
        return ParticleMetadata(name=self.__name)
