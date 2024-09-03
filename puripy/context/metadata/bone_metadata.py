from dataclasses import dataclass

from .metadata import Metadata


@dataclass
class BoneMetadata(Metadata):
    name: str
