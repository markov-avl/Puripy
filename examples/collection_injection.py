from typing import override

from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.marker import particle, factory


class Symbol:

    def __init__(self, character: str):
        self._character = character

    def __repr__(self):
        return self._character


@factory
class SymbolFactory:

    @particle
    def percent(self) -> Symbol:
        return Symbol("%")

    @particle
    def underscore(self) -> Symbol:
        return Symbol("_")

    @particle
    def dollar(self) -> Symbol:
        return Symbol("$")


class App(PuripyApplication):

    def __init__(self, symbol_list: list[Symbol], symbol_set: set[Symbol]):
        self._symbol_list = symbol_list
        self._symbol_set = symbol_set

    @override
    def run(self):
        print(f"List of injected symbols: {self._symbol_list}")
        print(f"Set of injected symbols: {self._symbol_set}")


if __name__ == "__main__":
    # >>> List of injected symbols: [%, _, $]
    # >>> Set of injected symbols: {_, %, $}
    PuripyApplicationRunner.run(App)
