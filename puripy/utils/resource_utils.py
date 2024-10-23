import warnings
from pathlib import Path

PROPERTY_FILE_PATTERN: str = "properties.*"


def find_property_files() -> list[Path]:
    root = Path('.')
    return list(root.glob(PROPERTY_FILE_PATTERN))


def get_property_file() -> Path:
    """
    :exception FileNotFoundError: If no default property file found
    """
    if not (paths := find_property_files()):
        raise FileNotFoundError("No default property file found")
    if len(paths) > 1:
        warnings.warn(f"More than one default property file found: {paths}; will be taken first")
    return paths[0]
