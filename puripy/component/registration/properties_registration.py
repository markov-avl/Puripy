from dataclasses import dataclass

from .registration import Registration


@dataclass
class PropertiesRegistration[T](Registration[T]):
    path: str
    prefix: str
