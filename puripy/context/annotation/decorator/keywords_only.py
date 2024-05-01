import functools
import inspect
from typing import Callable


class KeywordsOnly:
    """
    Removes the positional arguments, but tries to keep ``self`` and ``cls`` if provided as first argument.
    """

    def __new__[C: Callable](cls, function: C) -> C:
        def wrapper(*args, **kwargs):
            if cls._should_has_first_positional_argument(args, function):
                return function(args[0], **kwargs)
            return function(**kwargs)

        return wrapper

    @classmethod
    def _should_has_first_positional_argument(cls, args: tuple, f: Callable) -> bool:
        if not args or (c := cls._get_class_defined_method(f)) is None:
            return False

        return (args[0] if inspect.isclass(args[0]) else args[0].__class__) == c

    @classmethod
    def _get_class_defined_method(cls, f: Callable) -> type | None:
        if isinstance(f, functools.partial):
            return cls._get_class_defined_method(f.func)

        if inspect.ismethod(f) or inspect.isbuiltin(f) and hasattr(f, "__self__") and hasattr(f.__self__, "__class__"):
            for c in inspect.getmro(f.__self__.__class__):
                if f.__name__ in c.__dict__:
                    return c
            f = getattr(f, "__func__", f)

        if inspect.isfunction(f):
            class_name = f.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0]
            if (c := getattr(inspect.getmodule(f), class_name, None)) is not None and inspect.isclass(c):
                return c

        return getattr(f, "__objclass__", None)
