import inspect
from abc import ABC
from dataclasses import dataclass
from typing import Any


@dataclass
class Registration[T: type](ABC):
    constructor: Any
    params: list[inspect.Parameter]
    return_type: T
