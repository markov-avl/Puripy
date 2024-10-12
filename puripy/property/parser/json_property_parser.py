import json
from functools import cache
from typing import Any, override

from .property_parser import PropertyParser


class JsonPropertyParser(PropertyParser):

    @override
    def is_parseable(self, source: Any) -> bool:
        return isinstance(source, str) and source.endswith(".json")

    @override
    def parse(self, source: str) -> dict:
        return self.__parse(source)

    @staticmethod
    @cache
    def __parse(source: str) -> dict:
        with open(source, encoding="utf-8") as properties:
            return json.load(properties)
