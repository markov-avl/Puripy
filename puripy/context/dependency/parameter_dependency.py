from dataclasses import dataclass

from .dependency import Dependency


@dataclass
class ParameterDependency(Dependency):
    name: str
