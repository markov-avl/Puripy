from dataclasses import dataclass

from .containerized_registration import ContainerizedRegistration


@dataclass
class PropertiesRegistration(ContainerizedRegistration):
    path: str
    prefix: str
