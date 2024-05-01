from dataclasses import dataclass

from .metadata import Metadata


@dataclass
class ComponentMetadata(Metadata):
    name: str
