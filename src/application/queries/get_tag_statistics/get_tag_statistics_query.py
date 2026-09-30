from dataclasses import dataclass

from mediatorx import IQuery

from src.application.queries.get_tag_statistics.tag_statistics import TagStatistics


@dataclass(frozen=True, slots=True)
class GetTagStatisticsQuery(IQuery[TagStatistics]):
    tag: str
