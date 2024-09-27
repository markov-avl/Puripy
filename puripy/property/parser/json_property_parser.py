import json
from functools import cache
from typing import Any, override

from .property_parser import PropertyParser


class JsonPropertyParser(PropertyParser):

    @override
    def is_parseable(self, source: Any) -> bool:
        return isinstance(source, str) and source.endswith(".json")

    @cache
    @override
    def parse(self, source: str) -> dict:
        with open(source) as properties:
            return json.load(properties)
