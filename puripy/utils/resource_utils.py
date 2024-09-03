import warnings
from pathlib import Path
from typing import final


@final
class ResourceUtils:
    PROPERTY_FILE_PATTERN: str = "properties.*"

    @classmethod
    def find_property_files(cls) -> list[Path]:
        root = Path('.')
        return list(root.glob(cls.PROPERTY_FILE_PATTERN))

    @classmethod
    def get_property_file(cls) -> Path:
        """
        :exception RuntimeError: If no default property file found
        """
        paths = cls.find_property_files()
        if not paths:
            raise RuntimeError(f"No default property file found")
        if len(paths) > 1:
            warnings.warn(f"More than one default property file found: {paths}; will be taken first")
        return paths[0]
