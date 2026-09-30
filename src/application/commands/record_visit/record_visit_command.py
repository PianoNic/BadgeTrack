from dataclasses import dataclass

from mediatorx import ICommand

from src.application.commands.record_visit.recorded_visit import RecordedVisit


@dataclass(frozen=True, slots=True)
class RecordVisitCommand(ICommand[RecordedVisit]):
    tag: str
    label: str
    color: str
    style: str
    logo: str
    visitor_id: str | None
