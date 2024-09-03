from itertools import chain

from puripy.utils import BoneUtils

from .registration import BoneRegistration, PropertiesRegistration


class Registrar:

    def __init__[T](self):
        self._registry: dict[type[T], list[T]] = {}

    def register_bone[T](self, cls: T, name: str = "") -> None:
        registration = BoneRegistration(
            type=cls,
            name=BoneUtils.get_name(cls, name)
        )
        self._register(registration)

    def register_properties[T](self, cls: T, path: str, prefix: str, name: str = "") -> None:
        registration = PropertiesRegistration(
            type=cls,
            name=BoneUtils.get_name(cls, name),
            path=path,
            prefix=prefix
        )
        self._register(registration)

    def get_bones(self) -> list[BoneRegistration]:
        return self._registry[BoneRegistration]

    def get_properties(self) -> list[PropertiesRegistration]:
        return self._registry[PropertiesRegistration]

    def _register[T](self, registration: T) -> None:
        if registration.__class__ not in self._registry:
            self._registry[registration.__class__] = []
        self._registry[registration.__class__].append(registration)

    def __iter__(self):
        return iter(chain.from_iterable(self._registry.values()))
