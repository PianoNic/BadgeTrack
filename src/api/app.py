import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.types import Scope

from src.api.router_registry import router_registry
from src.infrastructure.configuration.environment_application_info_provider import (
    EnvironmentApplicationInfoProvider,
)
from src.infrastructure.dependency_injection import DEFAULT_DATABASE_PATH, build_mediator
from src.infrastructure.monitoring.sentry_error_reporter import SentryErrorReporter

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())

_FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
_BACKEND_PREFIXES = {"api", "badge", "docs", "openapi.json"}


class SpaStaticFiles(StaticFiles):
    # Any path that is not a built file gets index.html, so client-side routes survive a reload.
    # Backend paths still 404, otherwise a typo in an API call would come back as HTML.
    async def get_response(self, path: str, scope: Scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as error:
            if error.status_code != 404 or path.split("/", 1)[0] in _BACKEND_PREFIXES:
                raise
            return await super().get_response("index.html", scope)


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

    # mounted last so the API routes take precedence
    if _FRONTEND_DIST.is_dir():
        application.mount("/", SpaStaticFiles(directory=_FRONTEND_DIST, html=True), name="frontend")
    return application


app = create_app()
