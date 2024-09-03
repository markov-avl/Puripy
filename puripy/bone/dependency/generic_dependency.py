from dataclasses import dataclass
from typing import Any

from puripy.bone.registration import PropertiesRegistration, BoneRegistration

from .dependency import Dependency


@dataclass
class GenericDependency[T](Dependency):
    param_name: str
    generic_type: type[Any]
    registrations: list[PropertiesRegistration[T] | BoneRegistration[T]]
