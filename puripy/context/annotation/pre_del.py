from types import FunctionType

from .decorator import FunctionDecorator
from .context_annotation import ContextAnnotation


@FunctionDecorator
class PreDel[F: FunctionType](ContextAnnotation):

    def __call__(self, decoratable: F) -> F:
        decoratable.__pre_del__ = True

        return decoratable
