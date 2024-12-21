from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.marker import properties


@properties(path=".properties.yaml", prefix="example.simple")
class PythonEnvironmentVariables:
    python_home: str


class App(PuripyApplication):

    def __init__(self, python_environment_variables: PythonEnvironmentVariables):
        self._python_environment_variables = python_environment_variables

    async def run(self) -> None:
        print("PYTHONHOME:", self._python_environment_variables.python_home)


if __name__ == "__main__":
    # >>> PYTHONHOME: /usr/bin/python3
    PuripyApplicationRunner.run(App)
