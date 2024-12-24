from dataclasses import dataclass

from .metadata import Metadata


@dataclass
class ScanPackagesMetadata(Metadata):
    include: set[str]
    exclude: set[str]
