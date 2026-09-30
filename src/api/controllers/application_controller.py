import time

from fastapi import APIRouter, Depends
from mediatorx import Mediator

from src.api.controller import controller
from src.api.dependencies import get_mediator
from src.application.queries.get_application_info.application_info import ApplicationInfo
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)

router = APIRouter(tags=["App Info"])


@controller(router)
class ApplicationController:
    mediator: Mediator = Depends(get_mediator)

    @router.get("/api/app-info")
    async def get_application_info(self) -> dict[str, str]:
        info: ApplicationInfo = await self.mediator.send(GetApplicationInfoQuery())
        return {"environment": info.environment, "version": info.version}

    @router.get("/health")
    async def health(self) -> dict[str, object]:
        return {"status": "healthy", "timestamp": int(time.time())}
