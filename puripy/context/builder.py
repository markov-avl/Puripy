from typing import Any, get_args, get_origin

from puripy.utils.property_utils import get_property_file_path

from .annotation.comparator import AnnotationComparator
from .container import Container
from .dependency import ParameterDependency
from .property import PropertySourceReader
from .registrar import Registrar
from .registration import (ContainerizedRegistration,
                           PropertiesRegistration,
                           ParticleRegistration,
                           TemporaryRegistration,
                           Registration)


class Builder:

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
            r = self.__find_exactly_one_dependency_registration(dependency)
            self._construct_and_save(r, temporaries)

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
                kwargs[dependency.parameter_name] = self.__get_dependency_value(dependency, temporaries)
            except Exception as e:
                raise RuntimeError(f"Cannot obtain dependency value for '{registration.constructor}'", e)

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
                kwargs[dependency.parameter_name] = self.__get_dependency_value(dependency, {})
            except Exception as e:
                raise RuntimeError(f"Cannot obtain dependency value for '{registration.constructor}'", e)

        return registration.constructor(**kwargs)

    def __get_dependency_value(self, dependency: ParameterDependency, temporaries: dict[type, Any]) -> Any:
        if origin := get_origin(dependency.annotation):
            # FIXME: get rid of hardcode (set, frozenset, list)
            if origin in (set, frozenset, list):
                if args := get_args(dependency.annotation):
                    return origin(self.__container.get_by_type(args[0]))

                raise RuntimeError(
                    f"Too broad dependency annotation for '{dependency.parameter_name}': {dependency.annotation}"
                )

            raise RuntimeError(f"Unsupported dependency wrapper for '{dependency.parameter_name}': {origin}")

        try:
            registration = self.__find_exactly_one_dependency_registration(dependency)
        except Exception as e:
            raise RuntimeError(f"Cannot find dependency registration for '{dependency.parameter_name}'", e)

        if isinstance(registration, ContainerizedRegistration):
            return self.__container.get_by_name(registration.name)

        return temporaries.get(registration.return_type)

    def __find_exactly_one_dependency_registration(self, dependency: ParameterDependency) -> Registration:
        registrations = {
            dependency.parameter_name if isinstance(r, TemporaryRegistration) else r.name: r
            for r in self.__registrar
            if self.__annotation_comparator.is_subtype(r.return_type, dependency.annotation)
        }

        if not registrations:
            raise RuntimeError(f"No matching registrations found for parameter '{dependency.parameter_name}'")
        if len(registrations) == 1:
            return list(registrations.values())[0]
        if dependency.parameter_name in registrations:
            return registrations[dependency.parameter_name]

        raise RuntimeError(
            f"Multiple matching registrations found for parameter '{dependency.parameter_name}': {registrations}"
        )
