import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.router_registry import router_registry
from src.infrastructure.dependency_injection import DEFAULT_DATABASE_PATH, build_mediator

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())

_ROOT = Path(__file__).resolve().parents[2]


def create_app(database_path: Path | str = DEFAULT_DATABASE_PATH) -> FastAPI:
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
