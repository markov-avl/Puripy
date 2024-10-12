from dataclasses import dataclass

from .containerized_metadata import ContainerizedMetadata


@dataclass
class PropertiesMetadata(ContainerizedMetadata):
    path: str
    prefix: str
