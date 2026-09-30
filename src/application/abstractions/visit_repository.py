from typing import Protocol, runtime_checkable

from src.domain.models.visit_statistics import VisitStatistics


@runtime_checkable
class IVisitRepository(Protocol):
    def record_visit(self, tag: str, visitor_id: str) -> int: ...

    def get_visit_count(self, tag: str) -> int: ...

    def get_statistics(self) -> VisitStatistics: ...
