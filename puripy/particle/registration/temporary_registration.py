from dataclasses import dataclass

from .registration import Registration


@dataclass
class TemporaryRegistration[T: type](Registration):
    pass
