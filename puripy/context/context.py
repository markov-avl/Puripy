from __future__ import annotations

import inspect

from puripy.particle import Container, Registrar, Builder
from puripy.property import PropertySourceParser
from puripy.property.parser import JsonPropertyParser, YamlPropertyParser
from puripy.utils.containerized_utils import get_name
from puripy.utils.metadata_utils import is_particle, is_properties, get_exactly_one_metadata_of_type
from puripy.utils.reflection_utils import params_of, return_type_of
from puripy.utils.scan_utils import find_containerized, find_factories

from .assembler import Assembler
from .metadata import ParticleMetadata, PropertiesMetadata
from .post_processor import PostProcessor
from .pre_processor import PreProcessor


class Context:

    def __init__(self):
        self._container = Container()
        self._registrar = Registrar()
        self._builder = Builder(self._container, self._registrar)

    @property
    def container(self) -> Container:
        return self._container

    @property
    def registrar(self) -> Registrar:
        return self._registrar

    def initialize[T](self, application_type: type[T]) -> T:
        self._register_internals()
        self._registrar.register_particle(
            constructor=application_type,
            params=params_of(application_type),
            return_type=return_type_of(application_type),
            name=get_name(application_type)
        )

        acceptable_packages = {application_type.__module__.rsplit(".", 1)[0]}
        self._register_from_packages(acceptable_packages)

        assembler = Assembler(self._builder)
        assembler.assemble()

        post_processor = PostProcessor(self._container)
        post_processor.process_after_inits()

        return self._container.get_by_type(application_type)[0]

    def destroy(self) -> None:
        pre_processor = PreProcessor(self._container)
        pre_processor.process_before_dels()

    def _register_from_packages(self, packages: set[str]) -> None:
        for factory in find_factories(packages):
            self._registrar.register_temporary(
                constructor=factory,
                params=params_of(factory),
                return_type=return_type_of(factory)
            )

            for member in factory.__dict__.values():
                if is_particle(member):
                    metadata = get_exactly_one_metadata_of_type(member, ParticleMetadata)
                    params = params_of(member)
                    params[0] = params[0].replace(annotation=factory)
                    return_type = return_type_of(member)
                    self._registrar.register_particle(
                        constructor=member,
                        params=params,
                        return_type=return_type,
                        name=get_name(return_type, metadata.name)
                    )

        for containerized in find_containerized(packages):
            return_type = return_type_of(containerized)
            if is_particle(containerized):
                metadata = get_exactly_one_metadata_of_type(containerized, ParticleMetadata)
                self._registrar.register_particle(
                    constructor=containerized,
                    params=params_of(containerized),
                    return_type=return_type,
                    name=get_name(return_type, metadata.name)
                )
            elif is_properties(containerized):
                metadata = get_exactly_one_metadata_of_type(containerized, PropertiesMetadata)
                self._registrar.register_properties(
                    constructor=containerized,
                    params=params_of(containerized),
                    return_type=return_type,
                    name=get_name(return_type, metadata.name),
                    path=metadata.path,
                    prefix=metadata.prefix
                )

    def _register_internals(self) -> None:
        for particle in [JsonPropertyParser, YamlPropertyParser, PropertySourceParser]:
            self._registrar.register_particle(
                constructor=particle,
                params=params_of(particle),
                return_type=return_type_of(particle),
                name=get_name(particle)
            )
