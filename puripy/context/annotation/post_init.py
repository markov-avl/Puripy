from .decorator import FunctionDecorator
from .context_annotation import ContextAnnotation


@FunctionDecorator
class PostInit[Callable](ContextAnnotation):

    def __call__(self, decoratable):
        decoratable.__post_init__ = 934

        return decoratable
