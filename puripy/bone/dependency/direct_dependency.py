from dataclasses import dataclass

from puripy.bone.registration import PropertiesRegistration, BoneRegistration

from .dependency import Dependency


@dataclass
class DirectDependency[T](Dependency):
    param_name: str
    registration: PropertiesRegistration[T] | BoneRegistration[T]
