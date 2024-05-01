from .decorator import FunctionDecorator
from .context_annotation import ContextAnnotation


@FunctionDecorator
class PreDel[Callable](ContextAnnotation):

    def __call__(self, decoratable):
        decoratable.__pre_del__ = True

        return decoratable
