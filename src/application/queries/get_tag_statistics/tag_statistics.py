from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TagStatistics:
    tag: str
    visit_count: int
    last_updated: int
