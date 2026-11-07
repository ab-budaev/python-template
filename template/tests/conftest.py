import os

os.environ["OTEL_SDK_DISABLED"] = "true"

import fastapi
import pytest
from fastapi.testclient import TestClient

from main import app as _app


@pytest.fixture
def app() -> fastapi.FastAPI:
    return _app


@pytest.fixture
def test_client(app: fastapi.FastAPI) -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def test_client_raise_exceptions(app: fastapi.FastAPI) -> TestClient:
    return TestClient(app=app, raise_server_exceptions=True)
