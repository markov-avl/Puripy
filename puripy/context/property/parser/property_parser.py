from abc import ABC, abstractmethod
from typing import Any


class PropertyParser(ABC):

    @abstractmethod
    def is_parseable(self, source: Any) -> bool: ...

    @abstractmethod
    def parse(self, source: Any) -> dict: ...
