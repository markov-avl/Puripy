from __future__ import annotations

from inspect import signature, ismethod, isfunction
from dataclasses import dataclass
from typing import TypeVar, Callable, Union

T = TypeVar('T')


@dataclass
class _Constructor:
    kwargs: dict
    configurator: type | None = None


class Container:
    __instance: Container = None
    __initialized = False
    __container: dict[T, object] = dict()
    __constructors: dict[T, _Constructor] = dict()

    def __new__(cls, *args, **kwargs) -> Container:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __contains__(self, item):
        return item in self.__container

    def __repr__(self) -> str:
        return repr(self.__container)

    def __str__(self) -> str:
        return str(self.__container)

    @classmethod
    def component(cls, cls_: T = None, **cls_kwargs: any) -> T:
        if isinstance(cls_, type):
            cls.__constructors[cls_] = _Constructor(kwargs=cls_kwargs)
            return cls_

        def wrapper(cls__: type[T]) -> type[T]:
            return cls.component(cls__, **cls_kwargs)

        return wrapper

    @classmethod
    def configurator(cls, cls_: T = None, **cls_kwargs: any) -> T:
        if isinstance(cls_, type):
            cls._save_constructors(cls_, **cls_kwargs)
            return cls_

        def wrapper(cls__: type[T]) -> type[T]:
            return cls.configurator(cls__, **cls_kwargs)

        return wrapper

    @classmethod
    def get(cls, key: type[T]) -> T | None:
        return cls.__container.get(key, None)

    @classmethod
    def init(cls) -> None:
        for cls_ in cls.__constructors:
            cls._construct(cls_)

    @classmethod
    def _construct(cls, cls_: type) -> None:
        if cls_ not in cls.__constructors:
            return
        if cls.__constructors[cls_].configurator:
            configurator = cls._get_or_try_to_construct(cls.__constructors[cls_].configurator)
            configurator_method = cls._get_configuration_method(configurator, cls_)
            cls._try_to_construct_from_method(configurator_method)
        else:
            cls._try_to_construct_from_class(cls_)

    @classmethod
    def _try_to_construct_from_class(cls, cls_: type[T]) -> None:
        cls._try_to_construct_dependencies(cls_)
        kwargs = {**cls.__constructors[cls_].kwargs, **cls._get_kwargs_from_container(cls_)}
        cls.__container[cls_] = cls_(**kwargs)

    @classmethod
    def _try_to_construct_from_method(cls, method: Callable) -> None:
        return_type = signature(method).return_annotation
        cls._try_to_construct_dependencies(method)
        kwargs = {**cls.__constructors[return_type].kwargs, **cls._get_kwargs_from_container(method)}
        cls.__container[return_type] = method(**kwargs)

    @classmethod
    def _try_to_construct_dependencies(cls, obj: type | Callable) -> None:
        cls_ = signature(obj).return_annotation if cls._is_method(obj) else obj

        for param in signature(obj).parameters.values():
            if param.name in cls.__constructors[cls_].kwargs:
                continue
            if param.annotation in cls.__container:
                continue
            cls._construct(param.annotation)

    @classmethod
    def _get_or_try_to_construct(cls, cls_: type[T]) -> T:
        if cls_ not in cls.__container:
            cls._try_to_construct_from_class(cls_)
        return cls.__container[cls_]

    @classmethod
    def _get_kwargs_from_container(cls, obj: type | ()) -> dict[str, object]:
        return {
            param.name: cls.__container[param.annotation] for param in signature(obj).parameters.values()
            if param.annotation in cls.__container
        }

    @classmethod
    def _save_constructors(cls, cls_: type, **cls_kwargs: any) -> None:
        cls.__constructors[cls_] = _Constructor(kwargs=cls_kwargs)

        for method in cls._get_configuration_methods(cls_):
            return_type = signature(method).return_annotation
            cls.__constructors[return_type] = _Constructor(kwargs=dict(), configurator=cls_)

    @staticmethod
    def _is_method(attr: any) -> bool:
        return ismethod(attr) or isfunction(attr)

    @classmethod
    def _is_configuration_method(cls, configurator: type | object, attr_name: str) -> bool:
        attr = getattr(configurator, attr_name)

        return not attr_name.startswith('_') and not attr_name.endswith('_') and cls._is_method(attr)

    @classmethod
    def _get_configuration_methods(cls, configurator: type | object) -> list[Callable]:
        return [
            getattr(configurator, attr) for attr in dir(configurator)
            if cls._is_configuration_method(configurator, attr)
        ]

    @classmethod
    def _get_configuration_method(cls, configurator: type | object, return_type: type) -> Union[Callable, None]:
        return next(
            filter(
                lambda m: signature(m).return_annotation == return_type,
                cls._get_configuration_methods(configurator)
            ),
            None
        )