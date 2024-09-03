from types import FunctionType
from typing import final

from .decorator import functiondecorator
from .context_annotation import ContextAnnotation


# noinspection PyPep8Naming
@final
@functiondecorator
class postinit[F: FunctionType](ContextAnnotation):

    def __call__(self, decoratable: F) -> F:
        decoratable.__post_init__ = 934

        return decoratable
