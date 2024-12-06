from abc import ABC
from dataclasses import dataclass
from typing import Any

from puripy.context.dependency import Dependency, ParameterDependency


@dataclass
class Registration(ABC):
    constructor: Any
    dependencies: list[Dependency | ParameterDependency]
    return_type: type
