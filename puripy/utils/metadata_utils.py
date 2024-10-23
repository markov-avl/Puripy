from typing import Any

from puripy.context.metadata import (Metadata,
                                     DecoratorMetadata,
                                     AfterinitMetadata,
                                     BeforedelMetadata,
                                     ParticleMetadata,
                                     PropertiesMetadata,
                                     ContainerizedMetadata)

ATTRIBUTE_NAME = "__puripy__"


def append_metadata[M: Metadata](obj: Any, metadata: M) -> None:
    if hasattr(obj, ATTRIBUTE_NAME):
        getattr(obj, ATTRIBUTE_NAME).append(metadata)
    else:
        setattr(obj, ATTRIBUTE_NAME, [metadata])


def get_metadata[M: Metadata](obj: Any) -> list[M]:
    return getattr(obj, ATTRIBUTE_NAME, [])


def get_metadata_of_type[M: Metadata](obj: Any, metadata_type: type[M]) -> list[M]:
    return list(filter(lambda m: isinstance(m, metadata_type), get_metadata(obj)))


def get_only_one_metadata_of_type[M: Metadata](obj: Any, metadata_type: type[M]) -> M:
    metadata = get_metadata_of_type(obj, metadata_type)
    if len(metadata) != 1:
        raise ValueError(f"Cannot extract only one metadata from {obj} of type {metadata_type}. Found: {metadata}")
    return metadata[0]


def has_metadata_of_type[M: Metadata](obj: Any, metadata_type: type[M]) -> bool:
    return bool(get_metadata_of_type(obj, metadata_type))


def is_class_decorator(obj: Any) -> bool:
    return any(m.for_classes() for m in get_metadata_of_type(obj, DecoratorMetadata))


def is_function_decorator(obj: Any) -> bool:
    return any(m.for_functions() for m in get_metadata_of_type(obj, DecoratorMetadata))


def is_afterinit(obj: Any) -> bool:
    return has_metadata_of_type(obj, AfterinitMetadata)


def is_beforedel(obj: Any) -> bool:
    return has_metadata_of_type(obj, BeforedelMetadata)


def is_particle(obj: Any) -> bool:
    return has_metadata_of_type(obj, ParticleMetadata)


def is_properties(obj: Any) -> bool:
    return has_metadata_of_type(obj, PropertiesMetadata)


def is_containerized(obj: Any) -> bool:
    return has_metadata_of_type(obj, ContainerizedMetadata)
