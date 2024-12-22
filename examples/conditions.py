import math
from abc import ABC, abstractmethod
from typing import override

from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.marker import dependsonproperty, factory, particle


class IntegerHandler(ABC):

    @abstractmethod
    def handle(self, *ints: int) -> int: ...


class FloatHandler(ABC):

    @abstractmethod
    def handle(self, *floats: float) -> float: ...


@particle
@dependsonproperty(key="number-handler.type", value="sum", path=".properties.yaml")
class IntegerSummarizer(IntegerHandler):

    @override
    def handle(self, *ints: int) -> int:
        return sum(ints)


@particle
@dependsonproperty(key="number-handler.type", value="mul", path=".properties.yaml")
class IntegerMultiplier(IntegerHandler):

    @override
    def handle(self, *ints: int) -> int:
        return math.prod(ints)


@factory
class FloatHandlerFactory:

    @particle
    @dependsonproperty(key="number-handler.type", value="sum", path=".properties.yaml")
    def float_summarizer(self) -> FloatHandler:
        class FloatSummarizer(FloatHandler):

            @override
            def handle(self, *floats: float) -> float:
                return sum(floats)

        return FloatSummarizer()

    @particle
    @dependsonproperty(key="number-handler.type", value="mul", path=".properties.yaml")
    def float_multiplier(self) -> FloatHandler:
        class FloatMultiplier(FloatHandler):

            @override
            def handle(self, *floats: float) -> float:
                return round(math.prod(floats), 15)

        return FloatMultiplier()


class App(PuripyApplication):

    def __init__(self, integer_handler: IntegerHandler, float_handler: FloatHandler):
        self._integer_handler = integer_handler
        self._float_handler = float_handler

    @override
    def run(self) -> None:
        ints = [1, 2, 3, 4, 5]
        floats = [0.1, 0.2, 0.3, 0.4, 0.5]
        print(f"Result of handling {ints}: {self._integer_handler.handle(*ints)}")
        print(f"Result of handling {floats}: {self._float_handler.handle(*floats)}")


if __name__ == "__main__":
    # >>> Result of handling [1, 2, 3, 4, 5]: 120
    # >>> Result of handling [0.1, 0.2, 0.3, 0.4, 0.5]: 0.0012
    PuripyApplicationRunner.run(App)
