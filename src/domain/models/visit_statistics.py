from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VisitStatistics:
    total_tracked_tags: int
    total_visits: int
