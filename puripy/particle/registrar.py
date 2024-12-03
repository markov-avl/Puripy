import inspect
from itertools import chain

from puripy.utils.containerized_utils import get_name

from .registration import ParticleRegistration, PropertiesRegistration


class Registrar:

    def __init__[T](self):
        self._registry: dict[type[T], list[T]] = {}

    def register_particle[T](self, cls: T, name: str = "") -> None:
        return_type = inspect.signature(cls).return_annotation if inspect.isfunction(cls) else cls

        registration = ParticleRegistration(
            constructor=cls,
            return_type=return_type,
            name=get_name(cls, name)
        )
        self._register(registration)

    def register_properties[T](self, cls: T, path: str, prefix: str, name: str = "") -> None:
        registration = PropertiesRegistration(
            constructor=cls,
            return_type=cls,
            name=get_name(cls, name),
            path=path,
            prefix=prefix
        )
        self._register(registration)

    def get_particles(self) -> list[ParticleRegistration]:
        return self._registry[ParticleRegistration]

    def get_particles_of_type(self, particle_type: type) -> list[ParticleRegistration]:
        return list(filter(lambda r: issubclass(r.constructor, particle_type), self.get_particles()))

    def get_properties(self) -> list[PropertiesRegistration]:
        return self._registry[PropertiesRegistration]

    def _register[T](self, registration: T) -> None:
        if registration.__class__ not in self._registry:
            self._registry[registration.__class__] = []
        self._registry[registration.__class__].append(registration)

    def __iter__(self):
        return iter(chain.from_iterable(self._registry.values()))
