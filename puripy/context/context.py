from __future__ import annotations

from typing_extensions import LiteralString

from .builder import Builder
from .registrar import Registrar
from .container import Container
from puripy.context.property import PropertySourceReader
from puripy.context.property import JsonPropertyParser, YamlPropertyParser
from puripy.utils.containerized_utils import get_name
from puripy.utils.metadata_utils import is_particle, is_properties, get_exactly_one_metadata_of_type
from puripy.utils.reflection_utils import params_of, return_type_of
from puripy.utils.scan_utils import find_containerized, find_factories

from .assembler import Assembler
from .dependency import DependencyResolver
from puripy.context.annotation.comparator import AnnotationComparator
from puripy.context.annotation.comparator.generic import CollectionAnnotationComparator, UnionAnnotationComparator
from .metadata import ParticleMetadata, PropertiesMetadata
from .post_processor import PostProcessor
from .pre_processor import PreProcessor
from .scanning_packages_resolver import ScanningPackagesResolver


class Context:

    def __init__(self):
        self.__container = Container()
        self.__registrar = Registrar()
        self.__assembler = Assembler(self.__container, self.__registrar)
        self.__scanning_packages_resolver = ScanningPackagesResolver()

    @property
    def container(self) -> Container:
        return self.__container

    @property
    def registrar(self) -> Registrar:
        return self.__registrar

    def initialize[T](self, application_type: type[T]) -> T:
        self.__registrar.register_particle(
            constructor=application_type,
            dependencies=params_of(application_type),
            return_type=return_type_of(application_type),
            name=get_name(application_type)
        )

        scanning_packages = self.__scanning_packages_resolver.get_packages(application_type)
        self.__register_all_from_packages(scanning_packages)
        self.__assembler.assemble()

        post_processor = PostProcessor(self.__container)
        post_processor.process_after_inits()

        return self.__container.get_by_type(application_type)[0]

    def destroy(self) -> None:
        pre_processor = PreProcessor(self.__container)
        pre_processor.process_before_dels()

    def __register_all_from_packages(self, packages: set[str]) -> None:
        for factory in find_factories(packages):
            self.__registrar.register_temporary(
                constructor=factory,
                dependencies=params_of(factory),
                return_type=return_type_of(factory)
            )

            for member in factory.__dict__.values():
                if is_particle(member):
                    metadata = get_exactly_one_metadata_of_type(member, ParticleMetadata)
                    params = params_of(member)
                    params[0] = params[0].replace(annotation=factory)
                    return_type = return_type_of(member)
                    self.__registrar.register_particle(
                        constructor=member,
                        dependencies=params,
                        return_type=return_type,
                        name=get_name(return_type, metadata.name)
                    )

        for containerized in find_containerized(packages):
            return_type = return_type_of(containerized)
            if is_particle(containerized):
                metadata = get_exactly_one_metadata_of_type(containerized, ParticleMetadata)
                self.__registrar.register_particle(
                    constructor=containerized,
                    dependencies=params_of(containerized),
                    return_type=return_type,
                    name=get_name(return_type, metadata.name)
                )
            elif is_properties(containerized):
                metadata = get_exactly_one_metadata_of_type(containerized, PropertiesMetadata)
                self.__registrar.register_properties(
                    constructor=containerized,
                    dependencies=params_of(containerized),
                    return_type=return_type,
                    name=get_name(return_type, metadata.name),
                    path=metadata.path,
                    prefix=metadata.prefix
                )
