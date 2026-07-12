import collections
import inspect
import logging

from app.shared.dto.shared_dto import EventSubscribeDto, PublishEventDto


class EventDispatcher:
    def __init__(self) -> None:
        self._listeners = collections.defaultdict(list)
        self._logger = logging.getLogger(__name__)

    def subscribe(self, ctx: EventSubscribeDto):
        self._listeners[ctx.event_name].append(ctx.listener)
        self._logger.info(
            "Subscribed listener to event", extra={"event_name": ctx.event_name}
        )

    async def publish(self, ctx: PublishEventDto):
        self._logger.info(
            "Publishing event",
            extra={"event_name": ctx.event_name, "payload": ctx.payload},
        )

        for listener in self._listeners[ctx.event_name]:
            if inspect.iscoroutinefunction(listener):
                await listener(ctx.payload)
            else:
                listener(ctx.payload)


event_dispatcher = EventDispatcher()
