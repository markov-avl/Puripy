from dataclasses import dataclass
from typing import Any

from puripy.component.registration import PropertyHolderRegistration, ComponentRegistration

from .dependency import Dependency


@dataclass
class GenericDependency[T](Dependency):
    param_name: str
    generic_type: type[Any]
    registrations: list[PropertyHolderRegistration[T] | ComponentRegistration[T]]
