from typing import Any


class Container:

    def __init__(self):
        self._components: dict[str, Any] = {}

    def add_instance(self, name: str, instance: Any) -> None:
        """
        :exception ValueError: If the component name (ID) is already exist
        """
        if name in self._components:
            raise ValueError(f"Component name '{name}' (ID) is already exist")
        self._components[name] = instance

    def find_by_name[T](self, name: str) -> T | None:
        return self._components.get(name, None)

    def get_by_name[T](self, name: str) -> T:
        return self._components.get(name)

    def get_by_type[T](self, cls: type[T]) -> list[T]:
        return list(filter(lambda obj: isinstance(obj, cls), self._components.values()))

    def __iter__(self):
        return iter(self._components.items())
