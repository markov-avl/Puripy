from __future__ import annotations

from puripy.utils.containerized_utils import get_name
from puripy.utils.metadata_utils import is_particle, is_properties, get_exactly_one_metadata_of_type
from puripy.utils.reflection_utils import return_type_of
from puripy.utils.scan_utils import find_containerized, find_factories

from .assembler import Assembler
from .container import Container
from .dependency_resolver import DependencyResolver
from .metadata import ParticleMetadata, PropertiesMetadata
from .post_processor import PostProcessor
from .pre_processor import PreProcessor
from .registrar import Registrar
from .scanning_packages_resolver import ScanningPackagesResolver


class Context:

    def __init__(self):
        self.__container = Container()
        self.__registrar = Registrar()
        self.__dependency_resolver = DependencyResolver()
        self.__assembler = Assembler(self.__container, self.__registrar)

    @property
    def container(self) -> Container:
        return self.__container

    @property
    def registrar(self) -> Registrar:
        return self.__registrar

    def initialize[T](self, application_type: type[T]) -> T:
        self.__registrar.register_particle(
            constructor=application_type,
            dependencies=self.__dependency_resolver.get_dependencies(application_type),
            return_type=return_type_of(application_type),
            name=get_name(application_type)
        )

        packages_to_include, packages_to_exclude = ScanningPackagesResolver.of(application_type)
        self.__register_all_from_packages(packages_to_include, packages_to_exclude)
        self.__assembler.assemble()

        post_processor = PostProcessor(self.__container)
        post_processor.process_after_inits()

        return self.__container.get_by_type(application_type)[0]

    def destroy(self) -> None:
        pre_processor = PreProcessor(self.__container)
        pre_processor.process_before_dels()

    def __register_all_from_packages(self, packages_to_include: set[str], packages_to_exclude: set[str]) -> None:
        for factory in find_factories(packages_to_include, packages_to_exclude):
            self.__registrar.register_temporary(
                constructor=factory,
                dependencies=self.__dependency_resolver.get_dependencies(factory),
                return_type=return_type_of(factory)
            )

            for member in factory.__dict__.values():
                if is_particle(member):
                    metadata = get_exactly_one_metadata_of_type(member, ParticleMetadata)
                    return_type = return_type_of(member)
                    self.__registrar.register_particle(
                        constructor=member,
                        dependencies=self.__dependency_resolver.get_dependencies(member, factory),
                        return_type=return_type,
                        name=get_name(member, metadata.name)
                    )

        for containerized in find_containerized(packages_to_include, packages_to_exclude):
            return_type = return_type_of(containerized)
            if is_particle(containerized):
                metadata = get_exactly_one_metadata_of_type(containerized, ParticleMetadata)
                self.__registrar.register_particle(
                    constructor=containerized,
                    dependencies=self.__dependency_resolver.get_dependencies(containerized),
                    return_type=return_type,
                    name=get_name(return_type, metadata.name)
                )
            elif is_properties(containerized):
                metadata = get_exactly_one_metadata_of_type(containerized, PropertiesMetadata)
                self.__registrar.register_properties(
                    constructor=containerized,
                    dependencies=self.__dependency_resolver.get_dependencies(containerized),
                    return_type=return_type,
                    name=get_name(return_type, metadata.name),
                    path=metadata.path,
                    prefix=metadata.prefix
                )
