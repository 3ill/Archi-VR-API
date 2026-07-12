from app.shared.dto.shared_dto import EventSubscribeDto
from app.shared.event.event_definition import shared_events
from app.shared.event.event_dispatcher import event_dispatcher
from app.shared.service.email.email_service import EmailService


class EventSubscribers:
    def __init__(self) -> None:
        email_service = EmailService()
        event_dispatcher.subscribe(
            ctx=EventSubscribeDto(
                event_name=shared_events.SEND_WAITLIST_EMAIL,
                listener=email_service.send_waitlist_email,
            )
        )
