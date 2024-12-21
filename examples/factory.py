import asyncio
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

    @particle
    async def message(self) -> str:
        await asyncio.sleep(0.5)
        return "Just slept for 0.5 seconds"


class App(PuripyApplication):

    def __init__(self, python_path: Path, message: str):
        self._python_path = python_path
        self._message = message

    async def run(self) -> None:
        print(f"Path to python home: {self._python_path}")
        print(f"Message: {self._message}")


if __name__ == "__main__":
    # >>> Path to python home: /usr/bin/python3
    # >>> Message: Just slept for 0.5 seconds
    PuripyApplicationRunner.run(App)
