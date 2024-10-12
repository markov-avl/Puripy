from __future__ import annotations

from .metadata import Metadata


class AfterinitMetadata(Metadata):
    __INSTANCE: AfterinitMetadata = None

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__()

        if cls.__INSTANCE is None:
            cls.__INSTANCE = instance

        return instance

    @classmethod
    def instance(cls) -> AfterinitMetadata:
        return cls() if cls.__INSTANCE is None else cls.__INSTANCE
