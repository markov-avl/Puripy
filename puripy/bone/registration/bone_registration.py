from dataclasses import dataclass

from .registration import Registration


@dataclass
class BoneRegistration[T](Registration[T]):
    pass
