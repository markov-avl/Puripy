from typing import Any


class Container:

    def __init__(self):
        self.__items: dict[str, Any] = {}

    def add_instance(self, name: str, instance: Any) -> None:
        """
        :exception ValueError: If the particle name (ID) is already exist
        """

        if name in self.__items:
            raise ValueError(f"Particle name '{name}' (ID) is already exist")
        self.__items[name] = instance

    def find_by_name(self, name: str) -> Any | None:
        return self.__items.get(name, None)

    def get_by_name(self, name: str) -> Any:
        return self.__items.get(name)

    def get_by_type[T](self, cls: type[T]) -> list[T]:
        return list(filter(lambda obj: isinstance(obj, cls), self.__items.values()))

    def __iter__(self):
        return iter(self.__items.items())
