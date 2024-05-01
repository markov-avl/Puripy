from typing import Any

from puripy.property.parser import PropertyParser


class SourceParser:

    def __init__(self, parsers: list[PropertyParser]):
        self._parsers = parsers

    def parse(self, source: Any) -> dict:
        for parser in self._parsers:
            if parser.is_parseable(source):
                return parser.parse(source)
        raise RuntimeError(f"Property source {source} is unsupported")
