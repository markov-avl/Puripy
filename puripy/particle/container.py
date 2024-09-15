from typing import Any


class Container:

    def __init__(self):
        self._particles: dict[str, Any] = {}

    def add_instance(self, name: str, instance: Any) -> None:
        """
        :exception ValueError: If the particle name (ID) is already exist
        """
        if name in self._particles:
            raise ValueError(f"Particle name '{name}' (ID) is already exist")
        self._particles[name] = instance

    def find_by_name[T](self, name: str) -> T | None:
        return self._particles.get(name, None)

    def get_by_name[T](self, name: str) -> T:
        return self._particles.get(name)

    def get_by_type[T](self, cls: type[T]) -> list[T]:
        return list(filter(lambda obj: isinstance(obj, cls), self._particles.values()))

    def __iter__(self):
        return iter(self._particles.items())
