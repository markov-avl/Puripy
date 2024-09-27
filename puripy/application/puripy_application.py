from abc import ABC, abstractmethod


class PuripyApplication(ABC):

    @abstractmethod
    def run(self): ...
