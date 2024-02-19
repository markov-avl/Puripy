import builtins

from types import GenericAlias
from typing import Any, get_args

from puripy.utility import ResourceUtility, ReflectionUtility
from puripy.property import SourceParser

from .container import Container
from .dependency import DirectDependency, GenericDependency, IndirectDependency
from .registrar import Registrar
from .registration import PropertyHolderRegistration, ComponentRegistration

_Dependency = DirectDependency | GenericDependency | IndirectDependency
_Registration = PropertyHolderRegistration | ComponentRegistration


class Builder:

    def __init__(self, container: Container, registrar: Registrar):
        self._container = container
        self._registrar = registrar

    def build_registered(self) -> None:
        for registration in self._registrar:
            self._construct_and_save(registration)

    def _construct_and_save(self, registration: _Registration) -> None:
        if self._container.find_by_name(registration.name):
            return

        dependencies = self._get_registration_dependencies(registration)

        for dependency in dependencies:
            if isinstance(dependency, (DirectDependency, IndirectDependency)):
                self._construct_and_save(dependency.registration)
            if isinstance(dependency, GenericDependency):
                for dependency_registration in dependency.registrations:
                    self._construct_and_save(dependency_registration)

        if isinstance(registration, PropertyHolderRegistration):
            instance = self._property_holder(registration)
        elif isinstance(registration, ComponentRegistration):
            instance = self._component(registration, dependencies)
        else:
            raise TypeError(f"Unknown registration type: {registration.__class__}")

        self._container.add_instance(registration.name, instance)

    def _get_registration_dependencies(self, registration: _Registration) -> list[_Dependency]:
        if isinstance(registration, PropertyHolderRegistration):
            dependencies = [IndirectDependency(
                registration=next(filter(lambda r: issubclass(r.type, SourceParser), self._registrar.get_components()))
            )]
        else:
            dependencies = self._get_type_dependencies(registration.type)

        return dependencies

    def _get_type_dependencies(self, cls: type[Any]) -> list[_Dependency]:
        dependencies = []
        init_parameters = {param.name: param.annotation for param in ReflectionUtility.params_of(cls)}

        for param_name, param_annotation in init_parameters.items():
            if isinstance(param_annotation, GenericAlias):
                # TODO: remove hardcode (set, list)
                if not issubclass(param_annotation.__origin__, (set, list)):
                    raise RuntimeError(f"Unsupported dependency generic type for {cls}: {param_annotation.__origin__}")

                registrations = []

                # TODO: recursive realization (list[list[set[Any] | set[Any])
                for generic_type in get_args(param_annotation):
                    for registration in self._registrar:
                        if issubclass(registration.type, generic_type):
                            registrations.append(registration)

                dependencies.append(GenericDependency(
                    param_name=param_name,
                    generic_type=param_annotation.__origin__,
                    registrations=registrations
                ))
            else:
                registrations = {}

                for registration in self._registrar:
                    if issubclass(registration.type, param_annotation):
                        registrations[registration.name] = registration

                if not registrations:
                    RuntimeError(f"No matching dependencies found for {cls}: {param_name}[{param_annotation}]")
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

    def _property_holder[T](self, registration: PropertyHolderRegistration[T]) -> T:
        source = registration.path if registration.path else ResourceUtility.get_property_file().name
        source_parser = self._container.get_by_type(SourceParser)[0]
        properties = source_parser.parse(source)

        for prefix_path in filter(None, registration.prefix.split(".")):
            properties = properties[prefix_path]

        return registration.type(**properties)

    def _component[T](self, registration: ComponentRegistration[T], dependencies: list[_Dependency]) -> T:
        kwargs = {}

        for dependency in dependencies:
            if isinstance(dependency, DirectDependency):
                kwargs[dependency.param_name] = self._container.get_by_name(dependency.registration.name)
            elif isinstance(dependency, GenericDependency):
                injects = [self._container.get_by_name(r.name) for r in dependency.registrations]
                kwargs[dependency.param_name] = dependency.generic_type(injects)

        return registration.type(**kwargs)
