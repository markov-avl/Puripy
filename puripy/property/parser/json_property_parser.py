import json
from functools import cache
from typing import Any

from .property_parser import PropertyParser


class JsonPropertyParser(PropertyParser):

    def is_parseable(self, source: Any) -> bool:
        return isinstance(source, str) and source.endswith(".json")

    @cache
    def parse(self, source: str) -> dict:
        with open(source) as properties:
            return json.load(properties)
