import warnings
from pathlib import Path
from typing import final


@final
class ResourceUtility:
    PROPERTY_FILE_PATTERN: str = "properties.*"

    @staticmethod
    def find_property_files() -> list[Path]:
        root = Path('.')
        return list(root.glob(ResourceUtility.PROPERTY_FILE_PATTERN))

    @staticmethod
    def get_property_file() -> Path:
        """
        :exception RuntimeError: If no default property file found
        """
        paths = ResourceUtility.find_property_files()
        if not paths:
            raise RuntimeError(f"No default property file found")
        if len(paths) > 1:
            warnings.warn(f"More than one default property file found: {paths}; will be taken first")
        return paths[0]
