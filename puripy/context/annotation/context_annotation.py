from __future__ import annotations

from abc import ABC
from typing import Callable

from puripy.utility import ValidationUtility


class ContextAnnotation[C: Callable](ABC):

    def __new__(cls, *args, **kwargs) -> ContextAnnotation | C:
        annotation = super().__new__(cls)
        annotation.__init__(**kwargs)

        if args and callable(args[0]):
            ValidationUtility.validate_decoratable(annotation, args[0])
            return annotation(args[0])

        return annotation

    # *args should remain due PyCharm constructor argument list checkers
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, decoratable: C) -> C:
        return decoratable
