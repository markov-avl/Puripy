from dataclasses import dataclass

from puripy.particle.registration import PropertiesRegistration, ParticleRegistration

from .dependency import Dependency


@dataclass
class IndirectDependency[T](Dependency):
    registration: PropertiesRegistration[T] | ParticleRegistration[T]
