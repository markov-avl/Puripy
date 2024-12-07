from dataclasses import dataclass

from .dependency import Dependency


@dataclass
class IndirectDependency(Dependency):
    pass
