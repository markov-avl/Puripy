from pathlib import Path

from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.context.decorator.marker import factory, particle


@factory
class Factory:

    @particle
    def application_name(self) -> str:
        return "Configurator example"

    @particle
    def application_path(self) -> Path:
        return Path(__file__)


class App(PuripyApplication):

    def __init__(self, application_name: str, application_path: Path):
        self._application_name = application_name
        self._application_path = application_path

    async def run(self) -> None:
        print(f"Application name: {self._application_name}")
        print(f"Application file: {self._application_path.name}")


if __name__ == "__main__":
    # >>> Application name: Configurator example
    # >>> Application file: factory.py
    PuripyApplicationRunner.run(App)
