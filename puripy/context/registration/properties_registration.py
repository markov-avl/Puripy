from dataclasses import dataclass

from .registration import Registration


@dataclass
class PropertiesRegistration(Registration):
    name: str
    path: str
    prefix: str
