from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.context.annotation import afterinit, beforedel


class App(PuripyApplication):

    def __init__(self):
        print("__init__ call")

    def __del__(self):
        print("__del__ call")

    def run(self) -> None:
        print("Run call")

    @afterinit
    def after_init(self) -> None:
        print("After __init__ call")

    @beforedel
    def before_del(self) -> None:
        print("Before __del__ call")


if __name__ == '__main__':
    # >>> __init__ call
    # >>> After __init__ call
    # >>> Run call
    # >>> Before __del__ call
    # >>> __del__ call
    PuripyApplicationRunner.run(App)
