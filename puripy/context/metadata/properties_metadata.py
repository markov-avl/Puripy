from dataclasses import dataclass

from .metadata import Metadata


@dataclass
class PropertiesMetadata(Metadata):
    name: str
    path: str
    prefix: str
