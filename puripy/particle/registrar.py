import inspect
from itertools import chain
from types import FunctionType

from .registration import ParticleRegistration, PropertiesRegistration, TemporaryRegistration


class Registrar:

    def __init__[T](self):
        self._registry: dict[type[T], list[T]] = {}

    def register_temporary(self,
                           constructor: type,
                           params: list[inspect.Parameter],
                           return_type: type) -> None:
        registration = TemporaryRegistration(
            constructor=constructor,
            params=params,
            return_type=return_type
        )
        self._register(registration)

    def register_particle(self,
                          constructor: type | FunctionType,
                          params: list[inspect.Parameter],
                          return_type: type,
                          name: str) -> None:
        registration = ParticleRegistration(
            constructor=constructor,
            params=params,
            return_type=return_type,
            name=name
        )
        self._register(registration)

    def register_properties(self,
                            constructor: type,
                            params: list[inspect.Parameter],
                            return_type: type,
                            name: str,
                            path: str,
                            prefix: str) -> None:
        registration = PropertiesRegistration(
            constructor=constructor,
            params=params,
            return_type=return_type,
            name=name,
            path=path,
            prefix=prefix
        )
        self._register(registration)

    def get_particles(self) -> list[ParticleRegistration]:
        return self._registry[ParticleRegistration]

    def get_particles_of_type(self, particle_type: type) -> list[ParticleRegistration]:
        return list(filter(lambda r: issubclass(r.return_type, particle_type), self.get_particles()))

    def get_properties(self) -> list[PropertiesRegistration]:
        return self._registry[PropertiesRegistration]

    def get_properties_of_type(self, properties_type: type) -> list[ParticleRegistration]:
        return list(filter(lambda r: issubclass(r.return_type, properties_type), self.get_properties()))

    def _register[T](self, registration: T) -> None:
        if registration.__class__ not in self._registry:
            self._registry[registration.__class__] = []
        self._registry[registration.__class__].append(registration)

    def __iter__(self):
        return iter(chain.from_iterable(self._registry.values()))
