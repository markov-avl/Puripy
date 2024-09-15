import inspect
from typing import final

from puripy.context import Context
from puripy.utils import ParticleUtils
from .decorator import classdecorator
from .context_marker import ContextMarker


# noinspection PyPep8Naming
@final
@classdecorator
class particle[T: type](ContextMarker):

    def __init__(self, /, name: str = ""):
        super().__init__()
        self.__name = name

    def __call__(self, decoratable: T) -> T:
        if ParticleUtils.has_string_annotations(decoratable):
            raise RuntimeError(f"Particle {decoratable} has string-annotated dependencies. Is 'annotations' imported?")
        if ParticleUtils.has_empty_annotations(decoratable):
            raise RuntimeError(f"Particle {decoratable} has unknown-type dependencies. Annotate all params.")

        if inspect.isabstract(decoratable):
            raise RuntimeError("Abstract class cannot be a particle")

        context = Context()
        context.registrar.register_particle(decoratable, self.__name)

        return decoratable
