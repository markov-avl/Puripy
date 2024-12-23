import sys

from puripy.context.metadata import ScanPackagesMetadata
from puripy.utils.metadata_utils import find_metadata_of_type


class ScanningPackagesResolver:

    def __init__(self):
        self.__include: set[str] = set()
        self.__exclude: set[str] = set()

    def include_package(self, *package: str) -> None:
        self.__include.update(package)

    def exclude_package(self, *package: str) -> None:
        self.__exclude.update(package)

    def resolve_packages(self) -> set[str]:
        if conflicts := self.__include.intersection(self.__exclude):
            raise ValueError(f"The packages {conflicts} are listed as included and excluded packages")

        all_included = set()
        for pkg_name in self.__include:
            all_included.update(self.__collect_submodules(pkg_name))

        for pkg_name in self.__exclude:
            to_remove = self.__collect_submodules(pkg_name)
            all_included.difference_update(to_remove)

        return all_included

    @classmethod
    def of(cls, application_type: type) -> set[str]:
        resolver = cls()
        resolver.include_package(application_type.__module__.rsplit(".", 1)[0])

        for metadata in find_metadata_of_type(application_type, ScanPackagesMetadata):
            resolver.include_package(*metadata.include)
            resolver.exclude_package(*metadata.exclude)

        return resolver.resolve_packages()

    @staticmethod
    def __collect_submodules(pkg_name: str) -> set[str]:
        submodules = set()

        for module_name in sys.modules:
            if module_name == pkg_name or module_name.startswith(f"{pkg_name}."):
                submodules.add(module_name)

        if not submodules:
            submodules.add(pkg_name)

        return submodules
