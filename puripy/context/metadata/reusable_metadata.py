from __future__ import annotations

from abc import ABC
from typing import Self

from .metadata import Metadata


class ReusableMetadata(Metadata, ABC):
    __INSTANCE: ReusableMetadata = None

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__init__()

        if cls.__INSTANCE is None:
            cls.__INSTANCE = instance

        return instance

    @classmethod
    def instance(cls) -> Self:
        return cls() if cls.__INSTANCE is None else cls.__INSTANCE
