from puripy import PuripyApplication


class ScanningPackagesResolver:

    def __init__(self):
        self.__packages: set[str] = set()

    def add_package(self, package: str) -> None:
        self.__packages.add(package)

    def get_packages(self, application_type: PuripyApplication):
        return {application_type.__module__.rsplit(".", 1)[0], *self.__packages}
