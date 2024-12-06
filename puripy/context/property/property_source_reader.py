from typing import Any

from puripy.context.property.parser import PropertyParser


class PropertySourceReader:

    def __init__(self):
        self.__parsers: set[PropertyParser] = set()

    def add_parser(self, parser: PropertyParser) -> None:
        self.__parsers.add(parser)

    def read(self, property_source: Any) -> dict:
        for parser in self.__parsers:
            if parser.is_parseable(property_source):
                return parser.parse(property_source)
        raise RuntimeError(f"Property source {property_source} is unsupported")
