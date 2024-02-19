from dataclasses import dataclass

from .registration import Registration


@dataclass
class PropertyHolderRegistration[T](Registration[T]):
    path: str
    prefix: str
