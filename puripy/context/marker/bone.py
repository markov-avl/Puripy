import inspect
from typing import final

from puripy.context import Context
from puripy.utils import BoneUtils
from .decorator import classdecorator
from .context_marker import ContextMarker


# noinspection PyPep8Naming
@final
@classdecorator
class bone[T: type](ContextMarker):

    def __init__(self, /, name: str = ""):
        super().__init__()
        self.__name = name

    def __call__(self, decoratable: T) -> T:
        if BoneUtils.has_string_annotations(decoratable):
            raise RuntimeError(f"Bone {decoratable} has string-annotated dependencies. Is 'annotations' imported?")
        if BoneUtils.has_empty_annotations(decoratable):
            raise RuntimeError(f"Bone {decoratable} has unknown-type dependencies. Annotate all params.")

        if inspect.isabstract(decoratable):
            raise RuntimeError("Abstract class cannot be a bone")

        context = Context()
        context.registrar.register_bone(decoratable, self.__name)

        return decoratable
