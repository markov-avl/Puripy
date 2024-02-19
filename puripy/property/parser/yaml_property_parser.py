from functools import cache
from typing import Any

import yaml

from .property_parser import PropertyParser


class YamlPropertyParser(PropertyParser):

    def is_parseable(self, source: Any) -> bool:
        return isinstance(source, str) and (source.endswith(".yaml") or source.endswith(".yml"))

    @cache
    def parse(self, source: str) -> dict:
        with open(source) as properties:
            return yaml.load(properties, yaml.Loader)
