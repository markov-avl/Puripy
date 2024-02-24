import asyncio
import inspect

from puripy.component import Container


class PostProcessor:

    def __init__(self, container: Container):
        self._container = container

    def process_port_inits(self) -> None:
        post_inits = []
        for _, instance in self._container:
            instance_post_inits = [m for _, m in inspect.getmembers(instance) if getattr(m, "__post_init__", 0) == 934]
            if len(instance_post_inits) > 1:
                class_name = instance.__class__.__name__
                raise RuntimeError(f"More than one post initialization method found for '{class_name}'")
            if instance_post_inits:
                post_inits.append(instance_post_inits[0])

        for post_init in post_inits:
            if inspect.iscoroutinefunction(post_init):
                asyncio.get_event_loop().run_until_complete(post_init())
            else:
                post_init()
