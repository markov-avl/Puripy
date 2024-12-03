import inspect
from types import MethodType
from typing import final, override

from puripy.context.decorator import DecoratableType
from puripy.context.metadata import ParticleMetadata
from puripy.utils.reflection_utils import has_string_annotations, has_empty_annotations

from .marker import Marker


# noinspection PyPep8Naming
@final
class particle[T: type | MethodType](Marker):

    def __init__(self, /, name: str = ""):
        super().__init__([DecoratableType.CLASS, DecoratableType.FUNCTION, DecoratableType.METHOD])
        self.__name = name

    # @override
    # def __call__(self, decoratable: T) -> T:
    #     if has_string_annotations(decoratable):
    #         raise RuntimeError(f"Particle {decoratable} has string-annotated dependencies. Is 'annotations' imported?")
    #     if has_empty_annotations(decoratable):
    #         raise RuntimeError(f"Particle {decoratable} has unknown-type dependencies. Annotate all params.")
    #
    #     if inspect.isclass(decoratable) and inspect.isabstract(decoratable):
    #         raise RuntimeError("Abstract class cannot be a particle")
    #
    #     return super().__call__(decoratable)

    @override
    def _to_metadata(self) -> ParticleMetadata:
        return ParticleMetadata(name=self.__name)
