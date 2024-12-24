from collections.abc import Callable
from sys import modules
from typing import Any

from .metadata_utils import is_factory, is_containerized
from .reflection_utils import is_hashable


def find_objects(module_filter: Callable[[str], bool], object_filter: Callable[[Any], bool]) -> set[Any]:
    return {
        obj
        for module_name, module in modules.items() if module_filter(module_name)
        for obj in module.__dict__.values() if is_hashable(obj) and object_filter(obj)
    }


def find_objects_in_packages(object_filter: Callable[[Any], bool],
                             to_include: set[str] = None,
                             to_exclude: set[str] = None) -> set[Any]:
    if to_include is None and to_exclude is None:
        return find_objects(bool, object_filter)
    if not to_include:
        return set()

    if not to_exclude:
        def module_filter(m: str) -> bool:
            return is_defined_in_any(m, to_include)
    else:
        def module_filter(m: str) -> bool:
            return is_defined_in_any(m, to_include) and not is_defined_in_any(m, to_exclude)

    return find_objects(module_filter, object_filter)


def find_containerized(to_include: set[str] = None, to_exclude: set[str] = None) -> set[Any]:
    return find_objects_in_packages(is_containerized, to_include, to_exclude)


def find_factories(to_include: set[str] = None, to_exclude: set[str] = None) -> set[Any]:
    return find_objects_in_packages(is_factory, to_include, to_exclude)


def is_defined_in_any(module_name: str, packages: set[str]) -> bool:
    return any(module_name.startswith(package) for package in packages)
