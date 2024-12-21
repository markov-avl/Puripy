from functools import cache
from typing import override, Any, get_origin, get_args

from .generic_annotation_handler import GenericAnnotationHandler


class CollectionAnnotationHandler(GenericAnnotationHandler):

    @classmethod
    @cache
    @override
    def origins(cls) -> list[Any]:
        return [list, set, frozenset]

    @override
    def is_subtype(self, type1: Any, type2: Any, annotation_comparator) -> bool:
        origin1, origin2 = get_origin(type1), get_origin(type2)

        # if one of types is just a collection, then other may be handler of that type
        if type1 in self.origins() and type1 is origin2:
            return True
        if type2 in self.origins() and type2 is origin1:
            return True
        if origin1 is not origin2 or origin1 not in self.origins():
            return False

        args1, args2 = get_args(type1), get_args(type2)
        if len(args1) == 0 or len(args2) == 0:
            return True

        return annotation_comparator.is_subtype(args1[0], args2[0])
