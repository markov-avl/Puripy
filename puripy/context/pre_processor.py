import asyncio
import inspect

from puripy.bone import Container
from puripy.utils import MetadataUtils


class PreProcessor:

    def __init__(self, container: Container):
        self._container = container

    def process_before_dels(self) -> None:
        before_dels = []
        for _, instance in list(self._container)[::-1]:
            instance_before_dels = [m for _, m in inspect.getmembers(instance) if MetadataUtils.is_beforedel(m)]
            if len(instance_before_dels) > 1:
                class_name = instance.__class__.__name__
                raise RuntimeError(f"More than one before-deletion method found for '{class_name}'")
            if instance_before_dels:
                before_dels.append(instance_before_dels[0])

        for before_del in before_dels:
            if inspect.iscoroutinefunction(before_del):
                asyncio.get_event_loop().run_until_complete(before_del())
            else:
                before_del()
