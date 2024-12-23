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

    def resolve_packages(self) -> tuple[set[str], set[str]]:
        if conflicts := self.__include.intersection(self.__exclude):
            raise ValueError(f"The packages {conflicts} are listed as packages to include and exclude")

        return set(self.__include), set(self.__exclude)

    @classmethod
    def of(cls, application_type: type) -> tuple[set[str], set[str]]:
        resolver = cls()
        resolver.include_package(application_type.__module__.rsplit(".", 1)[0])

        for metadata in find_metadata_of_type(application_type, ScanPackagesMetadata):
            resolver.include_package(*metadata.include)
            resolver.exclude_package(*metadata.exclude)

        return resolver.resolve_packages()
