import asyncio
import inspect
from typing import final

from puripy.context import Context

from .puripy_application import PuripyApplication


@final
class PuripyApplicationRunner:

    @classmethod
    def run(cls, application_type: type[PuripyApplication]):
        if not issubclass(application_type, PuripyApplication):
            raise TypeError("Expected type extended from PuripyApplication")

        loop = asyncio.get_event_loop()
        context = Context()

        try:
            application = context.initialize(application_type)

            if inspect.iscoroutinefunction(application.run):
                loop.run_until_complete(application.run())
            else:
                application.run()
        except (KeyboardInterrupt, InterruptedError):
            pass
        finally:
            context.destroy()
            loop.close()
