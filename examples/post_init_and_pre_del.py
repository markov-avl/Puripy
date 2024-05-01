from puripy import PuripyApplication, PuripyApplicationRunner
from puripy.context.annotation import PostInit, PreDel


class App(PuripyApplication):

    def __init__(self):
        print("__init__ call")

    def __del__(self):
        print("__del__ call")

    def run(self) -> None:
        print("Run call")

    @PostInit
    def post_init(self) -> None:
        print("After __init__ call")

    @PreDel
    def pre_del(self) -> None:
        print("Before __del__ call")


if __name__ == '__main__':
    # >>> __init__ call
    # >>> After __init__ call
    # >>> Run call
    # >>> Before __del__ call
    # >>> __del__ call
    PuripyApplicationRunner.run(App)
