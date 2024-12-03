from collections.abc import Callable
from sys import modules
from typing import Any

from .metadata_utils import is_factory, is_containerized


def find_objects(module_filter: Callable[[str], bool], object_filter: Callable[[Any], bool]) -> set[Any]:
    return {
        obj
        for module_name, module in modules.items() if module_filter(module_name)
        for obj in module.__dict__.values() if object_filter(obj)
    }


def find_objects_in_packages(object_filter: Callable[[Any], bool], packages: set[str] = None) -> set[Any]:
    if packages is None:
        return find_objects(bool, object_filter)
    if not packages:
        return set()
    return find_objects(lambda m: is_defined_in_any(m, packages), object_filter)


def find_factories(packages: set[str] = None) -> set[Any]:
    return find_objects_in_packages(is_factory, packages)


def find_containerized(packages: set[str] = None) -> set[Any]:
    return find_objects_in_packages(is_containerized, packages)


def is_defined_in_any(module_name: str, packages: set[str]) -> bool:
    return any(module_name.startswith(package) for package in packages)
