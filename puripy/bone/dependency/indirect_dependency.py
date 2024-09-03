from dataclasses import dataclass

from puripy.bone.registration import PropertiesRegistration, BoneRegistration

from .dependency import Dependency


@dataclass
class IndirectDependency[T](Dependency):
    registration: PropertiesRegistration[T] | BoneRegistration[T]
