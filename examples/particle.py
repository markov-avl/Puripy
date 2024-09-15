from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.context.marker import particle


@particle
class ValueHolder:

    def __init__(self):
        self._value = "example value"

    @property
    def value(self) -> str:
        return self._value


class App(PuripyApplication):

    def __init__(self, value_holder: ValueHolder):
        self._value_holder = value_holder

    async def run(self) -> None:
        print("Held value:", self._value_holder.value)


if __name__ == '__main__':
    # >>> Held value: example value
    PuripyApplicationRunner.run(App)
