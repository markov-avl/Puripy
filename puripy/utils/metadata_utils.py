from typing import final, Any

from puripy.context.metadata import Metadata, DecoratorMetadata


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
    def is_class_decorator(cls, obj: Any) -> bool:
        decorator_metadata = cls.get_metadata_of_type(obj, DecoratorMetadata)
        return not decorator_metadata or any(m.for_classes() for m in decorator_metadata)

    @classmethod
    def is_function_decorator(cls, obj: Any) -> bool:
        decorator_metadata = cls.get_metadata_of_type(obj, DecoratorMetadata)
        return not decorator_metadata or any(m.for_functions() for m in decorator_metadata)
