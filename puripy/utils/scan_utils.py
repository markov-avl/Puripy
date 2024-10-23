import inspect
from sys import modules

from .reflection_utils import is_defined_in_any
from .metadata_utils import is_containerized


def find_containerized(acceptable_packages: set[str] = None) -> set[type]:
    containerized: set[type] = set()

    for module_name, module in modules.items():
        if not is_defined_in_any(module_name, acceptable_packages):
            continue
        for _, member in inspect.getmembers(module):
            if is_containerized(member):
                containerized.add(member)

    return containerized
