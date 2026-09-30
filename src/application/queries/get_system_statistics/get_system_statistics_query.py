from dataclasses import dataclass

from mediatorx import IQuery

from src.domain.models.visit_statistics import VisitStatistics


@dataclass(frozen=True, slots=True)
class GetSystemStatisticsQuery(IQuery[VisitStatistics]):
    pass
