import asyncio
import inspect

from puripy.bone import Container


class PreProcessor:

    def __init__(self, container: Container):
        self._container = container

    def process_pre_dels(self) -> None:
        pre_dels = []
        for _, instance in list(self._container)[::-1]:
            instance_pre_dels = [m for _, m in inspect.getmembers(instance) if hasattr(m, '__pre_del__')]
            if len(instance_pre_dels) > 1:
                class_name = instance.__class__.__name__
                raise RuntimeError(f"More than one pre deletion method found for '{class_name}'")
            if instance_pre_dels:
                pre_dels.append(instance_pre_dels[0])

        for pre_del in pre_dels:
            if inspect.iscoroutinefunction(pre_del):
                asyncio.get_event_loop().run_until_complete(pre_del())
            else:
                pre_del()
