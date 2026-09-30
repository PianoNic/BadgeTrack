from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecordedVisit:
    badge_url: str
    badge_svg: bytes | None
    visit_count: int
    new_visitor_id: str | None
