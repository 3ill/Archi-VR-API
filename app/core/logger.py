import logging
import logging.config
from datetime import datetime, timezone

from pythonjsonlogger import json

from app.core.request_context import request_id_ctx_var


class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_data, record, message_dict):
        super().add_fields(log_data, record, message_dict)

        log_data["level"] = record.levelname
        log_data["logger"] = record.name
        log_data["timestamp"] = datetime.now(timezone.utc).isoformat()

        request_id = request_id_ctx_var.get()
        if request_id:
            log_data["request_id"] = request_id

        log_data.pop("levelname", None)
        log_data.pop("name", None)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": CustomJsonFormatter,
            "format": "%(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
