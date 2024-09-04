from __future__ import annotations

from .metadata import Metadata


class BeforedelMetadata(Metadata):
    __INSTANCE = None

    @classmethod
    def instance(cls) -> BeforedelMetadata:
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE
