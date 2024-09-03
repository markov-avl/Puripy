from dataclasses import dataclass

from puripy.component.registration import PropertiesRegistration, ComponentRegistration

from .dependency import Dependency


@dataclass
class DirectDependency[T](Dependency):
    param_name: str
    registration: PropertiesRegistration[T] | ComponentRegistration[T]
