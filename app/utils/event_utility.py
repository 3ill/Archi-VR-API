import asyncio
import logging


class EventUtility:
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def fire_and_forget(self, coro, *, context: str):
        task = asyncio.create_task(coro)

        def _handle_task_result(t: asyncio.Task):
            try:
                exc = t.exception()
            except asyncio.CancelledError:
                return
            if exc:
                self._logger.error(
                    "Background task failed",
                    extra={"context": context, "error_type": type(exc).__name__},
                    exc_info=exc,
                )

        task.add_done_callback(_handle_task_result)
