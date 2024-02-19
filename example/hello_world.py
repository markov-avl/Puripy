from puripy import PuripyApplication, PuripyApplicationRunner


class App(PuripyApplication):

    async def run(self):
        print("Hello world!")


if __name__ == '__main__':
    PuripyApplicationRunner.run(App)
