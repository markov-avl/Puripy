from __future__ import annotations

from abc import ABC
from typing import Callable

from puripy.utils import ValidationUtils


class ContextAnnotation[C: Callable](ABC):

    def __new__(cls, *args, **kwargs) -> ContextAnnotation | C:
        annotation = super().__new__(cls)
        annotation.__init__(**kwargs)

        if args and callable(args[0]):
            ValidationUtils.validate_decoratable(annotation, args[0])
            return annotation(args[0])

        return annotation

    def __init__(self, /, **kwargs):
        pass

    def __call__(self, decoratable: C) -> C:
        return decoratable
