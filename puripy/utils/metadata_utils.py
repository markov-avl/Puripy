from typing import final, Any, Callable

from puripy.context.metadata import (Metadata,
                                     DecoratorMetadata,
                                     AfterinitMetadata,
                                     BeforedelMetadata,
                                     ParticleMetadata,
                                     PropertiesMetadata,
                                     ContainerizedMetadata)


@final
class MetadataUtils:
    ATTRIBUTE_NAME = "__puripy__"

    @classmethod
    def append_metadata[M: Metadata](cls, obj: Any, metadata: M) -> None:
        if hasattr(obj, cls.ATTRIBUTE_NAME):
            getattr(obj, cls.ATTRIBUTE_NAME).append(metadata)
        else:
            setattr(obj, cls.ATTRIBUTE_NAME, [metadata])

    @classmethod
    def get_metadata[M: Metadata](cls, obj: Any) -> list[M]:
        return getattr(obj, cls.ATTRIBUTE_NAME, [])

    @classmethod
    def get_metadata_of_type[M: Metadata](cls, obj: Any, metadata_type: type[M]) -> list[M]:
        return list(filter(lambda m: isinstance(m, metadata_type), cls.get_metadata(obj)))

    @classmethod
    def get_only_one_metadata_of_type[M: Metadata](cls, obj: Any, metadata_type: type[M]) -> M:
        metadata = cls.get_metadata_of_type(obj, metadata_type)
        if len(metadata) != 1:
            raise ValueError(f"Cannot extract only one metadata from {obj} of type {metadata_type}. Found: {metadata}")
        return metadata[0]

    @classmethod
    def has_metadata_of_type[M: Metadata](cls, obj: Any, metadata_type: type[M]) -> bool:
        return bool(cls.get_metadata_of_type(obj, metadata_type))

    @classmethod
    def is_class_decorator(cls, obj: Any) -> bool:
        return any(m.for_classes() for m in cls.get_metadata_of_type(obj, DecoratorMetadata))

    @classmethod
    def is_function_decorator(cls, obj: Any) -> bool:
        return any(m.for_functions() for m in cls.get_metadata_of_type(obj, DecoratorMetadata))

    @classmethod
    def is_afterinit(cls, obj: Any) -> bool:
        return cls.has_metadata_of_type(obj, AfterinitMetadata)

    @classmethod
    def is_beforedel(cls, obj: Any) -> bool:
        return cls.has_metadata_of_type(obj, BeforedelMetadata)

    @classmethod
    def is_particle(cls, obj: Any) -> bool:
        return cls.has_metadata_of_type(obj, ParticleMetadata)

    @classmethod
    def is_properties(cls, obj: Any) -> bool:
        return cls.has_metadata_of_type(obj, PropertiesMetadata)

    @classmethod
    def is_containerized(cls, obj: Any) -> bool:
        return cls.has_metadata_of_type(obj, ContainerizedMetadata)
