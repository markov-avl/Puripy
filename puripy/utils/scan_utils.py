import inspect
from dataclasses import dataclass
from types import ModuleType
from typing import final

from puripy.bone.registration import Registration, BoneRegistration, PropertiesRegistration
from puripy.context.metadata import PropertiesMetadata, ContainerizedMetadata
from puripy.utils import MetadataUtils, BoneUtils, ReflectionUtils


@final
class ScanUtils:
    @dataclass(unsafe_hash=True)
    class Source:
        module: ModuleType
        type: type

    @classmethod
    def scan_bones(cls, target: type, packages: set[str] = None) -> dict[str, Registration]:
        acceptable_packages = packages if packages else {target.__module__}
        scanned_bones = cls.__scan_bones_recursively(target, acceptable_packages, set(), dict())

        return {name: cls.__to_registration(name, source.type) for name, source in scanned_bones.items()}

    @classmethod
    def __scan_bones_recursively(cls,
                                 target: type,
                                 acceptable_packages: set[str],
                                 scanned_classes: set[Source],
                                 scanned_bones: dict[str, Source]) -> dict[str, Source]:
        if not inspect.isclass(target) or not ReflectionUtils.is_defined_in_any(target, acceptable_packages):
            return scanned_bones

        cls.__process_class(target, scanned_classes, scanned_bones)

        module = inspect.getmodule(target)
        for attr in dir(module):
            next_target = getattr(module, attr)
            cls.__scan_bones_recursively(next_target, acceptable_packages, scanned_classes, scanned_bones)

        return scanned_bones

    @classmethod
    def __process_class(cls, target: type, scanned_classes: set[Source], scanned_bones: dict[str, Source]) -> None:
        source = cls.Source(inspect.getmodule(target), target)
        if source in scanned_classes:
            return

        scanned_classes.add(source)

        if not MetadataUtils.is_containerized(target):
            return

        containerized_metadata = MetadataUtils.get_only_one_metadata_of_type(target, ContainerizedMetadata)
        bone_name = BoneUtils.get_name(target, containerized_metadata.name)

        if bone_name in scanned_bones:
            first = f"{scanned_bones[bone_name].module.__name__}.{scanned_bones[bone_name].type.__name__}"
            second = f"{source.module.__name__}.{source.type.__name__}"
            raise RuntimeError(f"Could not register 2 bones with the same name ({bone_name}): {first} and {second}")

        scanned_bones[bone_name] = source

    @staticmethod
    def __to_registration(name: str, type_: type) -> Registration:
        default_info = dict(name=name, type=type_)

        if MetadataUtils.is_bone(type_):
            return BoneRegistration(**default_info)
        if MetadataUtils.is_properties(type_):
            metadata = MetadataUtils.get_only_one_metadata_of_type(type_, PropertiesMetadata)
            return PropertiesRegistration(
                **default_info,
                path=metadata.path,
                prefix=metadata.prefix,
            )

        raise ValueError(f"Cannot map '{name}' of type {type_} to registration")
