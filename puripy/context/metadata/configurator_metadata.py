from __future__ import annotations

from .metadata import Metadata


class ConfiguratorMetadata(Metadata):
    __INSTANCE: ConfiguratorMetadata = None

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.__init__()

        if cls.__INSTANCE is None:
            cls.__INSTANCE = instance

        return instance

    @classmethod
    def instance(cls) -> ConfiguratorMetadata:
        return cls() if cls.__INSTANCE is None else cls.__INSTANCE
