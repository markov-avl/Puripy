from typing import Any

from puripy.context.metadata import (Metadata,
                                     AfterinitMetadata,
                                     BeforedelMetadata,
                                     ConfiguratorMetadata,
                                     ParticleMetadata,
                                     PropertiesMetadata,
                                     ContainerizedMetadata)

ATTRIBUTE_NAME = "__puripy__"


def append_metadata[M: Metadata](obj: Any, metadata: M) -> None:
    if hasattr(obj, ATTRIBUTE_NAME):
        getattr(obj, ATTRIBUTE_NAME).append(metadata)
    else:
        setattr(obj, ATTRIBUTE_NAME, [metadata])


def find_metadata[M: Metadata](obj: Any) -> list[M]:
    return getattr(obj, ATTRIBUTE_NAME, [])


def find_metadata_of_type[M: Metadata](obj: Any, metadata_type: type[M]) -> list[M]:
    return list(filter(lambda m: isinstance(m, metadata_type), find_metadata(obj)))


def get_exactly_one_metadata_of_type[M: Metadata](obj: Any, metadata_type: type[M]) -> M:
    metadata = find_metadata_of_type(obj, metadata_type)
    if len(metadata) != 1:
        raise ValueError(f"Cannot extract only one metadata from {obj} of type {metadata_type}. Found: {metadata}")
    return metadata[0]


def has_metadata_of_type[M: Metadata](obj: Any, metadata_type: type[M]) -> bool:
    return bool(find_metadata_of_type(obj, metadata_type))


def is_afterinit(obj: Any) -> bool:
    return has_metadata_of_type(obj, AfterinitMetadata)


def is_beforedel(obj: Any) -> bool:
    return has_metadata_of_type(obj, BeforedelMetadata)


def is_configurator(obj: Any) -> bool:
    return has_metadata_of_type(obj, ConfiguratorMetadata)


def is_particle(obj: Any) -> bool:
    return has_metadata_of_type(obj, ParticleMetadata)


def is_properties(obj: Any) -> bool:
    return has_metadata_of_type(obj, PropertiesMetadata)


def is_containerized(obj: Any) -> bool:
    return has_metadata_of_type(obj, ContainerizedMetadata)
