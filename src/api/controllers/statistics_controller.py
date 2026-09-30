from fastapi import APIRouter, Depends, HTTPException
from mediatorx import Mediator

from src.api.controller import controller
from src.api.dependencies import get_mediator
from src.application.queries.get_system_statistics.get_system_statistics_query import (
    GetSystemStatisticsQuery,
)
from src.application.queries.get_tag_statistics.get_tag_statistics_query import GetTagStatisticsQuery
from src.application.queries.get_tag_statistics.tag_statistics import TagStatistics
from src.domain.exceptions import InvalidBadgeError
from src.domain.models.visit_statistics import VisitStatistics

router = APIRouter(prefix="/api", tags=["Statistics"])


@controller(router)
class StatisticsController:
    mediator: Mediator = Depends(get_mediator)

    @router.get("/stats")
    async def get_system_statistics(self) -> dict[str, int]:
        stats: VisitStatistics = await self.mediator.send(GetSystemStatisticsQuery())
        return {"total_tracked_tags": stats.total_tracked_tags, "total_visits": stats.total_visits}

    @router.get("/stats/{tag}")
    async def get_tag_statistics(self, tag: str) -> dict[str, object]:
        try:
            stats: TagStatistics = await self.mediator.send(GetTagStatisticsQuery(tag=tag))
        except InvalidBadgeError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        return {"tag": stats.tag, "visit_count": stats.visit_count}
