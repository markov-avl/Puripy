from dataclasses import dataclass

from .registration import Registration


@dataclass
class ParticleRegistration[T](Registration[T]):
    pass
