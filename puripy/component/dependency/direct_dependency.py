from dataclasses import dataclass

from puripy.component.registration import PropertyHolderRegistration, ComponentRegistration

from .dependency import Dependency


@dataclass
class DirectDependency[T](Dependency):
    param_name: str
    registration: PropertyHolderRegistration[T] | ComponentRegistration[T]
