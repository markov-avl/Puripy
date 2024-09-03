from itertools import chain

from puripy.utils import ComponentUtils

from .registration import ComponentRegistration, PropertiesRegistration


class Registrar:

    def __init__[T](self):
        self._registry: dict[type[T], list[T]] = {}

    def register_component[T](self, cls: T, name: str = "") -> None:
        registration = ComponentRegistration(
            type=cls,
            name=ComponentUtils.get_name(cls, name)
        )
        self._register(registration)

    def register_properties[T](self, cls: T, path: str, prefix: str, name: str = "") -> None:
        registration = PropertiesRegistration(
            type=cls,
            name=ComponentUtils.get_name(cls, name),
            path=path,
            prefix=prefix
        )
        self._register(registration)

    def get_components(self) -> list[ComponentRegistration]:
        return self._registry[ComponentRegistration]

    def get_properties(self) -> list[PropertiesRegistration]:
        return self._registry[PropertiesRegistration]

    def _register[T](self, registration: T) -> None:
        if registration.__class__ not in self._registry:
            self._registry[registration.__class__] = []
        self._registry[registration.__class__].append(registration)

    def __iter__(self):
        return iter(chain.from_iterable(self._registry.values()))
