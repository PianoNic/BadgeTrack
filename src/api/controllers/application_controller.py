import time

from fastapi import APIRouter

from src.api.dependencies import MediatorDependency
from src.application.queries.get_application_info.application_info import ApplicationInfo
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)

router = APIRouter(tags=["App Info"])


@router.get("/api/app-info")
async def get_application_info(mediator: MediatorDependency) -> dict[str, str]:
    info: ApplicationInfo = await mediator.send(GetApplicationInfoQuery())
    return {"environment": info.environment, "version": info.version}


@router.get("/health")
async def health() -> dict[str, object]:
    return {"status": "healthy", "timestamp": int(time.time())}
