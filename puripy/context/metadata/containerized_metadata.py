from abc import ABC
from dataclasses import dataclass

from .metadata import Metadata


@dataclass
class ContainerizedMetadata(Metadata, ABC):
    name: str
