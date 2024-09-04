import asyncio
import inspect

from puripy.bone import Container
from puripy.utils import MetadataUtils


class PostProcessor:

    def __init__(self, container: Container):
        self._container = container

    def process_after_inits(self) -> None:
        after_inits = []
        for _, instance in self._container:
            instance_after_inits = [m for _, m in inspect.getmembers(instance) if MetadataUtils.is_afterinit(m)]
            if len(instance_after_inits) > 1:
                class_name = instance.__class__.__name__
                raise RuntimeError(f"More than one after-initialization method found for '{class_name}'")
            if instance_after_inits:
                after_inits.append(instance_after_inits[0])

        for after_init in after_inits:
            if inspect.iscoroutinefunction(after_init):
                asyncio.get_event_loop().run_until_complete(after_init())
            else:
                after_init()
