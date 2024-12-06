from dataclasses import dataclass
from types import GenericAlias


@dataclass
class Dependency:
    is_direct: bool
    type: type

    @property
    def is_generic(self) -> bool:
        return isinstance(self.type, GenericAlias)
