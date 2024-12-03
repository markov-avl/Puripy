from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass
class Registration[T: type](ABC):
    constructor: Any
    return_type: T
    name: str
