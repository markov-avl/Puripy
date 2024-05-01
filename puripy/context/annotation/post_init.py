from types import FunctionType

from .decorator import FunctionDecorator
from .context_annotation import ContextAnnotation


@FunctionDecorator
class PostInit[F: FunctionType](ContextAnnotation):

    def __call__(self, decoratable: F) -> F:
        decoratable.__post_init__ = 934

        return decoratable
