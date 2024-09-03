from puripy.bone import Builder


class Assembler:

    def __init__(self, builder: Builder):
        self._builder = builder

    def assemble(self) -> None:
        self._builder.build_registered()
