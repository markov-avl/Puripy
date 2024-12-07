from dataclasses import dataclass
from types import GenericAlias
from typing import Any


@dataclass
class Dependency:
    is_direct: bool
    annotation: Any

    @property
    def is_generic(self) -> bool:
        return isinstance(self.annotation, GenericAlias)
