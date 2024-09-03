import inspect
from typing import final

from puripy.context import Context
from puripy.utility import ComponentUtility
from .decorator import classdecorator
from .context_annotation import ContextAnnotation


# noinspection PyPep8Naming
@final
@classdecorator
class component[T: type](ContextAnnotation):

    def __init__(self, name: str = ""):
        super().__init__()
        self.__name = name

    def __call__(self, decoratable: T) -> T:
        if ComponentUtility.has_string_annotations(decoratable):
            raise RuntimeError(f"Component {decoratable} has string-annotated dependencies. Is 'annotations' imported?")
        if ComponentUtility.has_empty_annotations(decoratable):
            raise RuntimeError(f"Component {decoratable} has unknown-type dependencies. Annotate all params.")

        if inspect.isabstract(decoratable):
            raise RuntimeError("Abstract class cannot be a component")

        context = Context()
        context.registrar.register_component(decoratable, self.__name)

        return decoratable
