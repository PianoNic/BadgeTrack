import logging
import secrets

from src.application.abstractions.badge_image_fetcher import IBadgeImageFetcher
from src.application.abstractions.badge_url_builder import IBadgeUrlBuilder
from src.application.abstractions.visit_repository import IVisitRepository
from src.application.commands.record_visit.record_visit_command import RecordVisitCommand
from src.application.commands.record_visit.recorded_visit import RecordedVisit
from src.domain.models.badge_request import BadgeRequest

logger = logging.getLogger(__name__)


class RecordVisitCommandHandler:
    def __init__(
        self,
        repository: IVisitRepository,
        url_builder: IBadgeUrlBuilder,
        image_fetcher: IBadgeImageFetcher,
    ) -> None:
        self._repository = repository
        self._url_builder = url_builder
        self._image_fetcher = image_fetcher

    async def handle(self, command: RecordVisitCommand) -> RecordedVisit:
        request = BadgeRequest.parse(command.tag, command.label, command.color, command.style, command.logo)
        new_visitor_id = None if command.visitor_id else secrets.token_hex(16)
        visitor_id = command.visitor_id or new_visitor_id

        # a failing counter must never break a badge embedded in someone's README
        try:
            count = self._repository.record_visit(request.tag, visitor_id)
        except Exception:
            logger.exception("Recording a visit for %r failed", request.tag)
            count = self._repository.get_visit_count(request.tag)
            new_visitor_id = None

        badge_url = self._url_builder.build(request, count)
        return RecordedVisit(
            badge_url=badge_url,
            badge_svg=await self._image_fetcher.fetch(badge_url),
            visit_count=count,
            new_visitor_id=new_visitor_id,
        )
