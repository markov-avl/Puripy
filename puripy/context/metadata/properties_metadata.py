from dataclasses import dataclass

from .metadata import Metadata


@dataclass
class PropertiesMetadata(Metadata):
    path: str
    prefix: str
    name: str
