import inspect
from typing import final, Any, Callable

import inflection

from .reflection_utils import ReflectionUtils


@final
class ParticleUtils:

    @classmethod
    def get_name(cls, obj: Any, name: str = "") -> str:
        obj_name = obj.__name__ if inspect.isclass(obj) else obj.__class__.__name__
        return name if name else inflection.underscore(obj_name)

    @classmethod
    def has_incorrect_annotations(cls, obj: Callable) -> bool:
        return cls.has_string_annotations(obj) or cls.has_empty_annotations(obj)

    @classmethod
    def has_string_annotations(cls, obj: Callable) -> bool:
        return any(isinstance(param.annotation, str) for param in ReflectionUtils.params_of(obj))

    @classmethod
    def has_empty_annotations(cls, obj: Callable) -> bool:
        return any(issubclass(param.annotation, inspect.Parameter.empty) for param in ReflectionUtils.params_of(obj))
