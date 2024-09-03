from dataclasses import dataclass

from puripy.component.registration import PropertiesRegistration, ComponentRegistration

from .dependency import Dependency


@dataclass
class IndirectDependency[T](Dependency):
    registration: PropertiesRegistration[T] | ComponentRegistration[T]
