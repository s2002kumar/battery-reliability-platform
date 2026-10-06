"""Tests for architecture-independent repository foundations."""

import json
import logging
from pathlib import Path

import pytest

from battery_reliability.config import Settings
from battery_reliability.storage import StorageURI
from battery_reliability.structured_logging import JsonFormatter


def test_package_imports_from_src_layout() -> None:
    """The installed project package is importable from its src layout."""
    import battery_reliability

    assert battery_reliability.__version__ == "0.1.0"


def test_settings_defaults_and_environment_values() -> None:
    assert Settings.from_environment({}) == Settings()
    assert Settings.from_environment({"BRIP_ENV": "test", "BRIP_LOG_LEVEL": "debug"}) == Settings(
        environment="test", log_level="DEBUG"
    )


@pytest.mark.parametrize(
    ("key", "value"),
    [("BRIP_ENV", "staging"), ("BRIP_LOG_LEVEL", "TRACE")],
)
def test_settings_reject_unknown_values(key: str, value: str) -> None:
    with pytest.raises(ValueError):
        Settings.from_environment({key: value})


def test_storage_uri_accepts_local_paths_and_provider_uris() -> None:
    local_uri = StorageURI.from_path(Path.cwd() / "artifact.bin")
    remote_uri = StorageURI("s3://bucket/key")

    assert local_uri.scheme == "file"
    assert remote_uri.scheme == "s3"


def test_storage_uri_rejects_empty_or_relative_values() -> None:
    with pytest.raises(ValueError):
        StorageURI(" ")
    with pytest.raises(ValueError):
        StorageURI("relative/path")


def test_json_formatter_emits_selected_context_fields() -> None:
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="stage complete",
        args=(),
        exc_info=None,
    )
    record.stage = "test"
    record.artifact_id = "artifact-1"
    record.secret = "must not be serialized"

    payload = json.loads(JsonFormatter().format(record))

    assert payload["message"] == "stage complete"
    assert payload["stage"] == "test"
    assert payload["artifact_id"] == "artifact-1"
    assert "secret" not in payload
