from enum import Enum


class SharedEvents(str, Enum):
    SEND_WAITLIST_EMAIL = "send_waitlist_email"


shared_events = SharedEvents
