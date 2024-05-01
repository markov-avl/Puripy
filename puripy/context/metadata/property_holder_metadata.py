from dataclasses import dataclass

from .metadata import Metadata


@dataclass
class PropertyHolderMetadata(Metadata):
    name: str
    path: str
    prefix: str
