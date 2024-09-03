from typing import Any


class Container:

    def __init__(self):
        self._bones: dict[str, Any] = {}

    def add_instance(self, name: str, instance: Any) -> None:
        """
        :exception ValueError: If the bone name (ID) is already exist
        """
        if name in self._bones:
            raise ValueError(f"Bone name '{name}' (ID) is already exist")
        self._bones[name] = instance

    def find_by_name[T](self, name: str) -> T | None:
        return self._bones.get(name, None)

    def get_by_name[T](self, name: str) -> T:
        return self._bones.get(name)

    def get_by_type[T](self, cls: type[T]) -> list[T]:
        return list(filter(lambda obj: isinstance(obj, cls), self._bones.values()))

    def __iter__(self):
        return iter(self._bones.items())
