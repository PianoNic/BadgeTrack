from pathlib import Path

from mediatorx import DictResolver, Mediator

from src.application.commands.record_visit.record_visit_command import RecordVisitCommand
from src.application.commands.record_visit.record_visit_command_handler import RecordVisitCommandHandler
from src.application.queries.get_application_info.get_application_info_query import (
    GetApplicationInfoQuery,
)
from src.application.queries.get_application_info.get_application_info_query_handler import (
    GetApplicationInfoQueryHandler,
)
from src.application.queries.get_system_statistics.get_system_statistics_query import (
    GetSystemStatisticsQuery,
)
from src.application.queries.get_system_statistics.get_system_statistics_query_handler import (
    GetSystemStatisticsQueryHandler,
)
from src.application.queries.get_tag_statistics.get_tag_statistics_query import GetTagStatisticsQuery
from src.application.queries.get_tag_statistics.get_tag_statistics_query_handler import (
    GetTagStatisticsQueryHandler,
)
from src.infrastructure.badges.shields_badge_url_builder import ShieldsBadgeUrlBuilder
from src.infrastructure.configuration.environment_application_info_provider import (
    EnvironmentApplicationInfoProvider,
)
from src.infrastructure.persistence.peewee_visit_repository import PeeweeVisitRepository

DEFAULT_DATABASE_PATH = Path(__file__).resolve().parents[2] / "data" / "visitors.db"


def build_mediator(database_path: Path | str = DEFAULT_DATABASE_PATH) -> Mediator:
    repository = PeeweeVisitRepository(database_path)
    url_builder = ShieldsBadgeUrlBuilder()
    info_provider = EnvironmentApplicationInfoProvider()

    resolver = DictResolver()
    resolver.add_instance(RecordVisitCommandHandler, RecordVisitCommandHandler(repository, url_builder))
    resolver.add_instance(GetTagStatisticsQueryHandler, GetTagStatisticsQueryHandler(repository))
    resolver.add_instance(GetSystemStatisticsQueryHandler, GetSystemStatisticsQueryHandler(repository))
    resolver.add_instance(GetApplicationInfoQueryHandler, GetApplicationInfoQueryHandler(info_provider))

    mediator = Mediator(resolver=resolver)
    mediator.register(RecordVisitCommand, RecordVisitCommandHandler)
    mediator.register(GetTagStatisticsQuery, GetTagStatisticsQueryHandler)
    mediator.register(GetSystemStatisticsQuery, GetSystemStatisticsQueryHandler)
    mediator.register(GetApplicationInfoQuery, GetApplicationInfoQueryHandler)
    return mediator
