from functools import cache
from typing import Any, override

import yaml

from .property_parser import PropertyParser


class YamlPropertyParser(PropertyParser):

    @override
    def is_parseable(self, source: Any) -> bool:
        return isinstance(source, str) and (source.endswith(".yaml") or source.endswith(".yml"))

    @override
    def parse(self, source: str) -> dict:
        return self.__parse(source)

    @staticmethod
    @cache
    def __parse(source: str) -> dict:
        with open(source, encoding="utf-8") as properties:
            return yaml.load(properties, yaml.Loader)
