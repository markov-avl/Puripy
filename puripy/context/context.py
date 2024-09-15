from __future__ import annotations

from puripy.particle import Container, Registrar, Builder
from puripy.property import SourceParser
from puripy.property.parser import JsonPropertyParser, YamlPropertyParser

from .assembler import Assembler
from .post_processor import PostProcessor
from .pre_processor import PreProcessor


class Context:
    __instance: Context = None
    __initialized = False

    def __init__(self):
        if self.__initialized:
            return
        self._container = Container()
        self._registrar = Registrar()
        self._builder = Builder(self._container, self._registrar)
        self.__initialized = True

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @property
    def container(self) -> Container:
        return self._container

    @container.setter
    def container(self, container: Container) -> None:
        self._container = container

    @property
    def registrar(self) -> Registrar:
        return self._registrar

    @registrar.setter
    def registrar(self, registrar: Registrar) -> None:
        self._registrar = registrar

    def initialize[T](self, application_type: type[T]) -> T:
        self._register_internals()
        self._registrar.register_particle(application_type)

        assembler = Assembler(self._builder)
        assembler.assemble()

        post_processor = PostProcessor(self._container)
        post_processor.process_after_inits()

        return self._container.get_by_type(application_type)[0]

    def destroy(self) -> None:
        pre_processor = PreProcessor(self._container)
        pre_processor.process_before_dels()

    def _register_internals(self) -> None:
        self._registrar.register_particle(JsonPropertyParser)
        self._registrar.register_particle(YamlPropertyParser)
        self._registrar.register_particle(SourceParser)
