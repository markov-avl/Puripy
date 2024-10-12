from __future__ import annotations

from puripy.particle import Container, Registrar, Builder
from puripy.property import SourceParser
from puripy.property.parser import JsonPropertyParser, YamlPropertyParser
from puripy.utils import ScanUtils, MetadataUtils

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
        self._registrar.register_particle(application_type)

        acceptable_packages = {application_type.__module__.rsplit(".", 1)[0]}
        self._register_packages(acceptable_packages)

        assembler = Assembler(self._builder)
        assembler.assemble()

        post_processor = PostProcessor(self._container)
        post_processor.process_after_inits()

        return self._container.get_by_type(application_type)[0]

    def destroy(self) -> None:
        pre_processor = PreProcessor(self._container)
        pre_processor.process_before_dels()

    def _register_packages(self, packages: set[str]) -> None:
        for containerized in ScanUtils.find_containerized(packages):
            if MetadataUtils.is_particle(containerized):
                metadata = MetadataUtils.get_only_one_metadata_of_type(containerized, ParticleMetadata)
                self._registrar.register_particle(containerized, metadata.name)
            elif MetadataUtils.is_properties(containerized):
                metadata = MetadataUtils.get_only_one_metadata_of_type(containerized, PropertiesMetadata)
                self._registrar.register_properties(containerized, metadata.path, metadata.prefix, metadata.name)

    def _register_internals(self) -> None:
        self._registrar.register_particle(JsonPropertyParser)
        self._registrar.register_particle(YamlPropertyParser)
        self._registrar.register_particle(SourceParser)
