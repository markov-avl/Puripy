from abc import ABC
from dataclasses import dataclass


@dataclass
class Registration[T](ABC):
    type: type[T]
    name: str
