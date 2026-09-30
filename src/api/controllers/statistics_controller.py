from fastapi import APIRouter, HTTPException

from src.api.dependencies import MediatorDependency
from src.application.queries.get_system_statistics.get_system_statistics_query import (
    GetSystemStatisticsQuery,
)
from src.application.queries.get_tag_statistics.get_tag_statistics_query import GetTagStatisticsQuery
from src.application.queries.get_tag_statistics.tag_statistics import TagStatistics
from src.domain.exceptions import InvalidBadgeError
from src.domain.models.visit_statistics import VisitStatistics

router = APIRouter(prefix="/api", tags=["Statistics"])


@router.get("/stats")
async def get_system_statistics(mediator: MediatorDependency) -> dict[str, int]:
    stats: VisitStatistics = await mediator.send(GetSystemStatisticsQuery())
    return {
        "total_tracked_tags": stats.total_tracked_tags,
        "total_visits": stats.total_visits,
        "new_badges_today": stats.new_badges_today,
    }


@router.get("/stats/{tag}")
async def get_tag_statistics(tag: str, mediator: MediatorDependency) -> dict[str, object]:
    try:
        stats: TagStatistics = await mediator.send(GetTagStatisticsQuery(tag=tag))
    except InvalidBadgeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"tag": stats.tag, "visit_count": stats.visit_count, "last_updated": stats.last_updated}
