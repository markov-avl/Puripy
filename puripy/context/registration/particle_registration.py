from dataclasses import dataclass

from .registration import Registration


@dataclass
class ParticleRegistration(Registration):
    name: str
