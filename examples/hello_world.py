from typing import override

from puripy import PuripyApplication, PuripyApplicationRunner


class App(PuripyApplication):

    @override
    async def run(self) -> None:
        print("Hello world!")


if __name__ == "__main__":
    # >>> Hello world!
    PuripyApplicationRunner.run(App)
