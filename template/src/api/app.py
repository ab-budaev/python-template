from typing import Any

import fastapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from log import initialize_logging
from settings import AppSettings, get_settings
from telemetry import initialize_telemetry

from .routers import health_router


def create_app(
    *,
    settings: AppSettings | None = None,
    version: str = "0.1.0",
    description: str = "",
    **fastapi_kwargs: Any,
) -> fastapi.FastAPI:
    app_settings = settings if settings is not None else get_settings()

    initialize_logging(app_settings)
    initialize_telemetry(app_settings)

    app = fastapi.FastAPI(
        title=app_settings.app_name,
        version=version,
        description=description,
        **fastapi_kwargs,
    )
    app.state.settings = app_settings
    app.include_router(health_router)
    FastAPIInstrumentor.instrument_app(app)
    return app
