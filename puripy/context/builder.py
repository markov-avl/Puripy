import inspect
from types import GenericAlias
from typing import Any, get_args

from puripy.utils.property_utils import get_property_file_path

from .annotation.comparator import AnnotationComparator
from .container import Container
from .property import PropertySourceReader
from .registrar import Registrar
from .registration import PropertiesRegistration, ParticleRegistration, TemporaryRegistration

_Registration = PropertiesRegistration | ParticleRegistration | TemporaryRegistration


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

    def _construct_and_save(self, registration: _Registration, temporaries: dict[type, Any]) -> None:
        if isinstance(registration, TemporaryRegistration):
            if registration.return_type in temporaries:
                return
        elif self.__container.find_by_name(registration.name):
            return

        for dependency in registration.dependencies:
            if dependency.is_generic:
                for dependency_registration in dependency.registrations:
                    self._construct_and_save(dependency_registration, temporaries)
            else:
                self._construct_and_save(dependency.registration, temporaries)

        if isinstance(registration, PropertiesRegistration):
            instance = self._properties(registration)
            self.__container.add_instance(registration.name, instance)
        elif isinstance(registration, ParticleRegistration):
            instance = self._particle(registration, dependencies, temporaries)
            self.__container.add_instance(registration.name, instance)
        elif isinstance(registration, TemporaryRegistration):
            temporary = self._temporary(registration, dependencies)
            temporaries[registration.return_type] = temporary
        else:
            raise TypeError(f"Unknown registration type: {registration.__class__}")

    def _get_registration_dependencies(self, registration: _Registration) -> list[_Dependency]:
        if isinstance(registration, PropertiesRegistration):
            # properties are dependent only on property source parsers
            dependencies = [
                IndirectDependency(registration=r)
                for r in self.__registrar.get_particles_of_type(PropertySourceReader)
            ]
        else:
            dependencies = self._get_type_dependencies(registration.return_type, registration.dependencies)

        return dependencies

    def _get_type_dependencies(self, cls: type, params: list[inspect.Parameter]) -> list[_Dependency]:
        dependencies = []
        init_parameters = {param.name: param.annotation for param in params}

        for param_name, param_annotation in init_parameters.items():
            if isinstance(param_annotation, GenericAlias):
                # TODO: remove hardcode (set, list)
                if not issubclass(param_annotation.__origin__, (set, list, type)):
                    raise RuntimeError(f"Unsupported dependency generic type for {cls}: {param_annotation.__origin__}")

                registrations = []

                # TODO: recursive implementation (list[list[set[Any] | set[Any])
                for generic_type in get_args(param_annotation):
                    for registration in self.__registrar:
                        if issubclass(registration.return_type, generic_type):
                            registrations.append(registration)

                dependencies.append(GenericDependency(
                    param_name=param_name,
                    generic_type=param_annotation.__origin__,
                    registrations=registrations
                ))
            else:
                registrations = {}

                for registration in self.__registrar:
                    if issubclass(registration.return_type, param_annotation):
                        if isinstance(registration, TemporaryRegistration):
                            registrations[param_name] = registration
                        else:
                            registrations[registration.name] = registration

                if not registrations:
                    raise RuntimeError(f"No matching dependencies found for {cls}: {param_name}[{param_annotation}]")
                if len(registrations) == 1:
                    registration = list(registrations.values())[0]
                elif param_name in registrations:
                    registration = registrations[param_name]
                else:
                    raise RuntimeError(f"Cannot match dependency for {cls} by '{param_name}': {registrations}")

                dependencies.append(DirectDependency(
                    param_name=param_name,
                    registration=registration
                ))

        return dependencies

    def _properties(self, registration: PropertiesRegistration) -> Any:
        source = registration.path if registration.path else get_property_file_path().name
        properties = self.__property_source_reader.read(source)

        for prefix_path in filter(None, registration.prefix.split(".")):
            properties = properties[prefix_path]

        return registration.constructor(**properties)

    def _particle(self,
                  registration: ParticleRegistration,
                  dependencies: list[_Dependency],
                  temporaries: dict[type, Any]) -> Any:
        kwargs = {}

        for dependency in dependencies:
            if isinstance(dependency, DirectDependency):
                kwargs[dependency.param_name] = temporaries.get(dependency.registration.return_type) or \
                                                self.__container.find_by_name(dependency.registration.name)
            elif isinstance(dependency, GenericDependency):
                injects = [
                    temporaries.get(r.return_type) or self.__container.find_by_name(r.name)
                    for r in dependency.registrations
                ]
                kwargs[dependency.param_name] = dependency.generic_type(injects)

        return registration.constructor(**kwargs)

    def _temporary(self, registration: TemporaryRegistration, dependencies: list[_Dependency]) -> Any:
        kwargs = {}

        for dependency in dependencies:
            if isinstance(dependency, DirectDependency):
                kwargs[dependency.param_name] = self.__container.get_by_name(dependency.registration.name)
            elif isinstance(dependency, GenericDependency):
                injects = [self.__container.get_by_name(r.name) for r in dependency.registrations]
                kwargs[dependency.param_name] = dependency.generic_type(injects)

        return registration.constructor(**kwargs)
