from typing import override

from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.marker import scanpackages


@scanpackages(include="package.to.include", exclude="package.to.exclude")
class App(PuripyApplication):

    @override
    async def run(self) -> None:
        print("Hello world!")


if __name__ == "__main__":
    # >>> Hello world!
    PuripyApplicationRunner.run(App)
