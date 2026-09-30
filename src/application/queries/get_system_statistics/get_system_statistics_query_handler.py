from src.application.abstractions.visit_repository import IVisitRepository
from src.application.queries.get_system_statistics.get_system_statistics_query import (
    GetSystemStatisticsQuery,
)
from src.domain.models.visit_statistics import VisitStatistics


class GetSystemStatisticsQueryHandler:
    def __init__(self, repository: IVisitRepository) -> None:
        self._repository = repository

    async def handle(self, _query: GetSystemStatisticsQuery) -> VisitStatistics:
        return self._repository.get_statistics()
