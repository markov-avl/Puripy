from collections.abc import Callable

from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.context.decorator.marker import particle


@particle
def value_formatter() -> Callable[[str], str]:
    return str.upper


@particle
class ValueHolder:

    def __init__(self):
        self._value = "example value"

    @property
    def value(self) -> str:
        return self._value


class App(PuripyApplication):

    def __init__(self, value_holder: ValueHolder, value_formatter1: Callable[[str], str]):
        self._value_holder = value_holder
        self._value_formatter = value_formatter1

    async def run(self) -> None:
        print("Held value:", self._value_formatter(self._value_holder.value))


if __name__ == "__main__":
    # >>> Held value: example value
    PuripyApplicationRunner.run(App)
