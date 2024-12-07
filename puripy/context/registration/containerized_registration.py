from abc import ABC
from dataclasses import dataclass

from .registration import Registration


@dataclass
class ContainerizedRegistration(Registration, ABC):
    name: str
