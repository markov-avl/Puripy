from dataclasses import dataclass

from puripy.particle.registration import PropertiesRegistration, ParticleRegistration

from .dependency import Dependency


@dataclass
class DirectDependency[T](Dependency):
    param_name: str
    registration: PropertiesRegistration[T] | ParticleRegistration[T]
