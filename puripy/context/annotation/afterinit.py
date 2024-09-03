from types import FunctionType
from typing import final

from .decorator import functiondecorator
from .context_annotation import ContextAnnotation


# noinspection PyPep8Naming
@final
@functiondecorator
class afterinit[F: FunctionType](ContextAnnotation):

    def __call__(self, decoratable: F) -> F:
        decoratable.__afterinit__ = True

        return decoratable
