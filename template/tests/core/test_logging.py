import json
import logging

import pytest
import structlog

from log import initialize_logging
from settings import AppSettings


def _log_probe() -> None:
    structlog.get_logger().info("probe")


def _reset_logging() -> None:
    logging.getLogger().handlers = []
    structlog.reset_defaults()


def test_production_logs_json(capsys: pytest.CaptureFixture[str]) -> None:
    initialize_logging(AppSettings(app_name="test-app", app_env="testing", app_debug=False))

    _log_probe()
    captured = capsys.readouterr()

    record = json.loads(captured.err.strip().splitlines()[-1])
    assert record["event"] == "probe"
    assert record["level"] == "info"
    _reset_logging()


def test_debug_logs_console(capsys: pytest.CaptureFixture[str]) -> None:
    initialize_logging(AppSettings(app_name="test-app", app_env="testing", app_debug=True))

    _log_probe()
    captured = capsys.readouterr()

    output = captured.err
    assert "probe" in output
    assert "\x1b[" in output
    _reset_logging()
