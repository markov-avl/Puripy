from sys import modules

from .reflection_utils import is_defined_in_any
from .metadata_utils import is_configurator, is_containerized


def find_configurators(acceptable_packages: set[str] = None) -> set[type]:
    configurators: set[type] = set()

    for module_name, module in modules.items():
        if acceptable_packages is not None and not is_defined_in_any(module_name, acceptable_packages):
            continue
        for member in module.__dict__.values():
            if is_configurator(member):
                configurators.add(member)

    return configurators


def find_containerized(acceptable_packages: set[str] = None) -> set[type]:
    containerized: set[type] = set()

    for module_name, module in modules.items():
        if acceptable_packages is not None and not is_defined_in_any(module_name, acceptable_packages):
            continue
        for member in module.__dict__.values():
            if is_containerized(member):
                containerized.add(member)

    return containerized
