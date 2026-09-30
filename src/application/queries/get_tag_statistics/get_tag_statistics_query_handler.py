import time

from src.application.abstractions.visit_repository import IVisitRepository
from src.application.queries.get_tag_statistics.get_tag_statistics_query import GetTagStatisticsQuery
from src.application.queries.get_tag_statistics.tag_statistics import TagStatistics
from src.domain.exceptions import InvalidBadgeError

_MAX_TAG_LENGTH = 200


class GetTagStatisticsQueryHandler:
    def __init__(self, repository: IVisitRepository) -> None:
        self._repository = repository

    async def handle(self, query: GetTagStatisticsQuery) -> TagStatistics:
        if not query.tag or len(query.tag) > _MAX_TAG_LENGTH:
            raise InvalidBadgeError("Invalid tag parameter")
        return TagStatistics(
            tag=query.tag,
            visit_count=self._repository.get_visit_count(query.tag),
            last_updated=int(time.time()),
        )
