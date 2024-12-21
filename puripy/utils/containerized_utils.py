from typing import Any

import inflection

from .reflection_utils import defined_name


def get_name(obj: Any, name: str = "") -> str:
    return name if name else inflection.underscore(defined_name(obj))
