from pathlib import Path

from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.marker import factory, particle, properties


@properties(path=".properties.yaml", prefix="example.env-or-default")
class PythonEnvironmentVariables:
    python_home: str


@factory
class Factory:

    def __init__(self, python_environment_variables: PythonEnvironmentVariables):
        self._python_environment_variables = python_environment_variables

    @particle
    def python_path(self) -> Path:
        return Path(self._python_environment_variables.python_home)


class App(PuripyApplication):

    def __init__(self, python_path: Path):
        self._python_path = python_path

    async def run(self) -> None:
        print(f"This application : {self._python_path}")


if __name__ == "__main__":
    # >>> Application name: Configurator example
    # >>> Application file: factory.py
    PuripyApplicationRunner.run(App)
