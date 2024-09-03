from abc import ABC
from dataclasses import dataclass


@dataclass
class Registration[T: type](ABC):
    type: T
    name: str
