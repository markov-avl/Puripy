from __future__ import annotations

from .metadata import Metadata


class AfterinitMetadata(Metadata):
    __INSTANCE = None

    @classmethod
    def instance(cls) -> AfterinitMetadata:
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE
