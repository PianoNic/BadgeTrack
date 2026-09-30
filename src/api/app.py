import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.router_registry import router_registry
from src.infrastructure.configuration.environment_application_info_provider import (
    EnvironmentApplicationInfoProvider,
)
from src.infrastructure.dependency_injection import DEFAULT_DATABASE_PATH, build_mediator
from src.infrastructure.monitoring.sentry_error_reporter import SentryErrorReporter

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())

_ROOT = Path(__file__).resolve().parents[2]


def create_app(database_path: Path | str = DEFAULT_DATABASE_PATH) -> FastAPI:
    info = EnvironmentApplicationInfoProvider()
    SentryErrorReporter(os.getenv("SENTRY_DSN"), info.get_environment(), info.get_version()).initialize()

    application = FastAPI(
        title="BadgeTrack",
        description="Visitor counter badges for READMEs and websites",
        version="1.0.0",
    )
    application.state.mediator = build_mediator(database_path)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    router_registry.auto_register(application)

    application.mount("/static", StaticFiles(directory=_ROOT / "static"), name="static")
    application.mount("/assets", StaticFiles(directory=_ROOT / "assets"), name="assets")
    return application


app = create_app()
