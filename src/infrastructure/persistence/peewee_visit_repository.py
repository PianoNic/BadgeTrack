import logging
import time
from pathlib import Path

from peewee import SqliteDatabase, fn

from src.domain.models.visit_statistics import VisitStatistics
from src.infrastructure.persistence.peewee_models import Badge, Cookie

logger = logging.getLogger(__name__)


class PeeweeVisitRepository:
    def __init__(self, database_path: Path | str) -> None:
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        self._database = SqliteDatabase(str(database_path))
        self._database.bind([Badge, Cookie])
        self._database.create_tables([Badge, Cookie], safe=True)
        self._drop_legacy_visitor_index()
        logger.info("Database ready at %s", database_path)

    def _drop_legacy_visitor_index(self) -> None:
        # Databases created before #18 made cookie_id unique on its own, so a visitor could only ever
        # be counted on the first badge they saw. Uniqueness is per (cookie_id, badge) now.
        for index in self._database.get_indexes(Cookie._meta.table_name):
            if index.unique and index.columns == ["cookie_id"]:
                self._database.execute_sql(f'DROP INDEX "{index.name}"')
                logger.info("Dropped legacy unique index %s", index.name)

    def record_visit(self, tag: str, visitor_id: str) -> int:
        now = int(time.time())
        with self._database.atomic():
            badge, _ = Badge.get_or_create(tag=tag, defaults={"created": now})
            _, is_new_visitor = Cookie.get_or_create(
                cookie_id=visitor_id, badge=badge, defaults={"last_visit": now}
            )
            if is_new_visitor:
                badge.visits += 1
                badge.save()
            return badge.visits

    def get_visit_count(self, tag: str) -> int:
        badge = Badge.get_or_none(Badge.tag == tag)
        return badge.visits if badge else 0

    def get_statistics(self) -> VisitStatistics:
        return VisitStatistics(
            total_tracked_tags=Badge.select().count(),
            total_visits=Badge.select(fn.SUM(Badge.visits)).scalar() or 0,
        )
