from abc import ABC, abstractmethod
from typing import Any


class GenericAnnotationComparator(ABC):

    @classmethod
    @abstractmethod
    def origins(cls) -> list[Any]: ...

    @abstractmethod
    def is_subtype(self, type1: Any, type2: Any, annotation_comparator) -> bool: ...
