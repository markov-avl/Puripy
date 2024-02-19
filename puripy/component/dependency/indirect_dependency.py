from dataclasses import dataclass

from puripy.component.registration import PropertyHolderRegistration, ComponentRegistration

from .dependency import Dependency


@dataclass
class IndirectDependency[T](Dependency):
    registration: PropertyHolderRegistration[T] | ComponentRegistration[T]
