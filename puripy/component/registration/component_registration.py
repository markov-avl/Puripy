from dataclasses import dataclass

from .registration import Registration


@dataclass
class ComponentRegistration[T](Registration[T]):
    pass
