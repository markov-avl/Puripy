from itertools import chain
from typing import Any, get_origin

from .handler import GenericAnnotationHandler


class AnnotationComparator:

    def __init__(self):
        self.__generic_annotation_comparators: list[GenericAnnotationHandler] = []
        self.__equivalent_types: dict[Any, list[Any]] = {}

    def add_generic_annotation_comparator(self, comparator: GenericAnnotationHandler) -> None:
        """
        Adds a handler for handler comparison.

        :param comparator: The comparator to handle handler type comparisons.
        """

        self.__generic_annotation_comparators.append(comparator)

    def add_equivalent_types(self, base_type: Any, *equivalents: Any) -> None:
        """
        Adds equivalent types for a single base type.

        :param base_type: The base type to which the equivalents are added.
        :param equivalents: Variable number of equivalent types to be added for the base type.
        """

        if base_type not in self.__equivalent_types:
            self.__equivalent_types[base_type] = []
        self.__equivalent_types[base_type].extend(equivalents)

    def is_equals(self, type1: Any, type2: Any) -> bool:
        """
        Checks if two types are equivalent.

        :param type1: The first type to compare.
        :param type2: The second type to compare.
        :return: True if the types are equivalent, False otherwise.
        """

        if type1 is type2 or type1 == type2:
            return True

        equivalents1 = self.__equivalent_types.get(type1, [])
        equivalents2 = self.__equivalent_types.get(type2, [])

        return type1 in equivalents2 or type2 in equivalents1

    def is_subtype(self, type1: Any, type2: Any) -> bool:
        """
        :param type1: Base type to compare.
        :param type2: Type to compare for a subtype of type1.
        :return: True if type1 is a subtype of type2, False otherwise.
        :raises RuntimeError: If one of the types is not supported by the comparator.
        """

        if self.is_equals(type1, type2):
            return True

        # check for issubclass relationship if applicable
        if isinstance(type1, type) and isinstance(type2, type):
            return issubclass(type1, type2)

        supported_origins = self.__supported_generic_origins()
        if (origin1 := get_origin(type1)) and origin1 not in supported_origins:
            raise RuntimeError(f"Unsupported dependency handler type: {origin1}")
        if (origin2 := get_origin(type2)) and origin2 not in supported_origins:
            raise RuntimeError(f"Unsupported dependency handler type: {origin2}")

        # check through handler comparators
        return any(c.is_subtype(type1, type2, self) for c in self.__generic_annotation_comparators)

    def __supported_generic_origins(self) -> list[Any]:
        return list(chain.from_iterable(c.origins() for c in self.__generic_annotation_comparators))
