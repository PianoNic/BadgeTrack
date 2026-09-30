from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecordedVisit:
    badge_url: str
    visit_count: int
    new_visitor_id: str | None
