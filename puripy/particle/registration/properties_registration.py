from dataclasses import dataclass

from .registration import Registration


@dataclass
class PropertiesRegistration[T](Registration[T]):
    name: str
    path: str
    prefix: str
