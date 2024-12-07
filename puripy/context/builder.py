from typing import Any, get_args, get_origin

from puripy.utils.property_utils import get_property_file_path

from .annotation.comparator import AnnotationComparator
from .container import Container
from .dependency import ParameterDependency
from .property import PropertySourceReader
from .registrar import Registrar
from .registration import (ContainerizedRegistration,
                           ParticleRegistration,
                           PropertiesRegistration,
                           TemporaryRegistration,
                           Registration)

_RegistrationType = ParticleRegistration | PropertiesRegistration | TemporaryRegistration


class Builder:
    # FIXME: get rid of hardcode (set, frozenset, list)
    __SUPPORTED_WRAPPERS = {set, frozenset, list}

    def __init__(self,
                 container: Container,
                 registrar: Registrar,
                 annotation_comparator: AnnotationComparator,
                 property_source_reader: PropertySourceReader):
        self.__container = container
        self.__registrar = registrar
        self.__annotation_comparator = annotation_comparator
        self.__property_source_reader = property_source_reader

    def build_registered(self) -> None:
        temporaries: dict[type, Any] = {}
        for registration in self.__registrar:
            self._construct_and_save(registration, temporaries)

    def _construct_and_save(self, registration: Registration, temporaries: dict[type, Any]) -> None:
        if isinstance(registration, ContainerizedRegistration) and self.__container.find_by_name(registration.name):
            return
        if registration.return_type in temporaries:
            return

        for dependency in registration.dependencies:
            registry = self.__get_dependency_registrations(dependency)
            if isinstance(registry, list):
                for r in registry:
                    self._construct_and_save(r, temporaries)
            else:
                self._construct_and_save(registry, temporaries)

        if isinstance(registration, PropertiesRegistration):
            properties = self.__build_properties(registration)
            self.__container.add_instance(registration.name, properties)
        elif isinstance(registration, ParticleRegistration):
            particle = self.__build_particle(registration, temporaries)
            self.__container.add_instance(registration.name, particle)
        elif isinstance(registration, TemporaryRegistration):
            temporary = self.__build_temporary(registration)
            temporaries[registration.return_type] = temporary
        else:
            raise TypeError(f"Unknown registration type: {registration.__class__}")

    def __build_particle(self, registration: ParticleRegistration, temporaries: dict[type, Any]) -> Any:
        kwargs = {}

        for dependency in registration.dependencies:
            if not isinstance(dependency, ParameterDependency):
                continue
            try:
                kwargs[dependency.name] = self.__get_dependency_value(dependency, temporaries)
            except Exception as e:
                raise RuntimeError(f"Cannot obtain dependency value for '{registration.constructor}'") from e

        return registration.constructor(**kwargs)

    def __build_properties(self, registration: PropertiesRegistration) -> Any:
        source = registration.path if registration.path else get_property_file_path().name
        properties = self.__property_source_reader.read(source)

        for prefix_path in filter(None, registration.prefix.split(".")):
            properties = properties[prefix_path]

        return registration.constructor(**properties)

    def __build_temporary(self, registration: TemporaryRegistration) -> Any:
        kwargs = {}

        for dependency in registration.dependencies:
            if not isinstance(dependency, ParameterDependency):
                continue
            try:
                kwargs[dependency.name] = self.__get_dependency_value(dependency, {})
            except Exception as e:
                raise RuntimeError(f"Cannot obtain dependency value for '{registration.constructor}'") from e

        return registration.constructor(**kwargs)

    def __get_dependency_value(self, dependency: ParameterDependency, temporaries: dict[type, Any]) -> Any:
        try:
            registry = self.__get_dependency_registrations(dependency)
        except Exception as e:
            raise RuntimeError(f"Cannot find dependency registration(s) for '{dependency.name}'") from e

        if isinstance(registry, list):
            origin = get_origin(dependency.annotation)
            return origin(self.__container.get_by_name(r.name) for r in registry)

        if isinstance(registry, ContainerizedRegistration):
            return self.__container.get_by_name(registry.name)

        return temporaries.get(registry.return_type)

    def __find_registrations(self, annotation: Any) -> list[_RegistrationType]:
        return [
            r for r in self.__registrar
            if self.__annotation_comparator.is_subtype(r.return_type, annotation)
        ]

    def __get_dependency_registration(self, dependency: ParameterDependency) -> _RegistrationType:
        registrations = {
            dependency.name if isinstance(r, TemporaryRegistration) else r.name: r
            for r in self.__find_registrations(dependency.annotation)
        }

        if not registrations:
            raise RuntimeError(f"No matching registrations found for parameter '{dependency.name}'")
        if len(registrations) == 1:
            return list(registrations.values())[0]
        if dependency.name in registrations:
            return registrations[dependency.name]

        raise RuntimeError(
            f"Multiple matching registrations found for parameter '{dependency.name}': {registrations}"
        )

    def __get_dependency_registrations(self,
                                       dependency: ParameterDependency) -> _RegistrationType | list[_RegistrationType]:
        try:
            return self.__get_dependency_registration(dependency)
        except RuntimeError as e:
            if not dependency.is_generic():
                raise e
            if not (origin := get_origin(dependency.annotation)) in self.__SUPPORTED_WRAPPERS:
                raise RuntimeError(f"Unsupported generic wrapper type for '{dependency.name}': {origin}")
            if not (args := get_args(dependency.annotation)):
                raise RuntimeError(f"Too broad dependency annotation for '{dependency.name}': {origin}")
            return self.__find_registrations(args[0])
