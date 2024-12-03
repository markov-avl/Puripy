from typing import Any

from puripy.property.parser import PropertyParser


class PropertySourceParser:

    def __init__(self, parsers: list[PropertyParser]):
        self._parsers = parsers

    def parse(self, property_source: Any) -> dict:
        for parser in self._parsers:
            if parser.is_parseable(property_source):
                return parser.parse(property_source)
        raise RuntimeError(f"Property source {property_source} is unsupported")
