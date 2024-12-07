from typing import LiteralString

from .annotation.comparator import AnnotationComparator
from .annotation.comparator.handler import CollectionAnnotationHandler, UnionAnnotationHandler
from .builder import Builder
from .container import Container
from .property import PropertySourceReader
from .property.parser import JsonPropertyParser, YamlPropertyParser
from .registrar import Registrar


class Assembler:

    def __init__(self, container: Container, registrar: Registrar):
        self.__annotation_comparator = AnnotationComparator()
        self.__property_source_reader = PropertySourceReader()
        self.__builder = Builder(
            container=container,
            registrar=registrar,
            annotation_comparator=self.__annotation_comparator,
            property_source_reader=self.__property_source_reader
        )

    def assemble(self) -> None:
        self.__initialize_internals()
        self.__builder.build_registered()

    def __initialize_internals(self) -> None:
        # annotation comparator
        self.__annotation_comparator.add_generic_annotation_comparator(CollectionAnnotationHandler())
        self.__annotation_comparator.add_generic_annotation_comparator(UnionAnnotationHandler())
        self.__annotation_comparator.add_equivalent_types(str, LiteralString)
        # property source parser
        self.__property_source_reader.add_parser(JsonPropertyParser())
        self.__property_source_reader.add_parser(YamlPropertyParser())
