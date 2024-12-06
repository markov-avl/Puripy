from functools import cache
from typing import override, Any, get_origin, get_args, Union

from .generic_annotation_comparator import GenericAnnotationComparator


class UnionAnnotationComparator(GenericAnnotationComparator):

    @classmethod
    @cache
    @override
    def origins(cls) -> list[Any]:
        # pylint: disable=consider-alternative-union-syntax
        return [Union]

    @override
    def is_subtype(self, type1: Any, type2: Any, annotation_comparator) -> bool:
        origin1, origin2 = get_origin(type1), get_origin(type2)
        args1, args2 = set(get_args(type1)), set(get_args(type2))

        if origin1 is None and origin2 in self.origins():
            return all(annotation_comparator.is_equals(type1, argtype) for argtype in args2)
        if origin2 is None and origin1 in self.origins():
            return all(annotation_comparator.is_equals(type2, argtype) for argtype in args1)

        if not any(origin1 is o and origin2 is o for o in self.origins()):
            return False

        return args1 == args2
