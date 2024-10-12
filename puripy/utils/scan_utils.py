import inspect
from typing import final
from sys import modules

from puripy.utils import MetadataUtils, ReflectionUtils


@final
class ScanUtils:

    @classmethod
    def find_containerized(cls, acceptable_packages: set[str] = None) -> set[type]:
        containerized: set[type] = set()

        for module_name, module in modules.items():
            if not ReflectionUtils.is_defined_in_any(module_name, acceptable_packages):
                continue
            for _, member in inspect.getmembers(module):
                if MetadataUtils.is_containerized(member):
                    containerized.add(member)

        return containerized
