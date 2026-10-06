"""Typed application settings loaded from environment variables."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

Environment = Literal["development", "test", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Small validated settings object with no battery-domain configuration."""

    environment: Environment = "development"
    log_level: LogLevel = "INFO"

    @classmethod
    def from_environment(cls, environ: Mapping[str, str]) -> "Settings":
        """Build settings from the supplied environment mapping."""
        raw_environment = environ.get("BRIP_ENV", "development")
        raw_log_level = environ.get("BRIP_LOG_LEVEL", "INFO").upper()

        if raw_environment not in ("development", "test", "production"):
            raise ValueError("BRIP_ENV must be development, test, or production")
        if raw_log_level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            raise ValueError("BRIP_LOG_LEVEL must be a standard Python log level")

        return cls(
            environment=cast(Environment, raw_environment),
            log_level=cast(LogLevel, raw_log_level),
        )
