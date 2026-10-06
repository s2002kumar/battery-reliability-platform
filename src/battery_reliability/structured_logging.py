"""JSON logging setup for machine-readable application logs."""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from battery_reliability.config import LogLevel

_CONTEXT_FIELDS = ("source", "artifact_id", "run_id", "stage", "failure_reason")


class JsonFormatter(logging.Formatter):
    """Format log records as one JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        """Serialize the stable log envelope and selected operational context."""
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in _CONTEXT_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_logging(level: LogLevel) -> None:
    """Configure the root logger to emit structured JSON to standard error."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)
