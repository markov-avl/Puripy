from dataclasses import dataclass
from typing import Any

from .metadata import Metadata


@dataclass
class DependsOnPropertyMetadata(Metadata):
    key: str
    value: Any
    match_on_missing: bool
    path: str
