import asyncio
import os
import sys
import tempfile
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.application.commands.record_visit.record_visit_command import RecordVisitCommand
from src.infrastructure.dependency_injection import build_mediator


def temp_database() -> str:
    # a file, not ":memory:": peewee opens one connection per thread and the test client serves on another
    return os.path.join(tempfile.mkdtemp(), "visitors.db")


def client() -> TestClient:
    return TestClient(create_app(temp_database()), follow_redirects=False)


def count_in(location: str) -> str:
    return urlparse(location).path.split("/")[-1].split("-")[1]


def test_badge_redirects_to_shields_and_sets_a_visitor_cookie():
    response = client().get("/badge", params={"tag": "readme", "color": "237e61", "logo": "github"})
    assert response.status_code == 302
    location = response.headers["location"]
    assert location.startswith("https://img.shields.io/badge/visits-1-237e61.svg")
    assert parse_qs(urlparse(location).query) == {"style": ["flat"], "logo": ["github"]}
    assert response.headers["cache-control"].startswith("no-store")
    assert "visitor_id=" in response.headers["set-cookie"]


def test_a_visitor_is_counted_once_per_tag():
    browser = client()
    assert count_in(browser.get("/badge", params={"tag": "once"}).headers["location"]) == "1"
    assert count_in(browser.get("/badge", params={"tag": "once"}).headers["location"]) == "1"
    browser.cookies.clear()
    assert count_in(browser.get("/badge", params={"tag": "once"}).headers["location"]) == "2"


def test_invalid_parameters_are_rejected():
    browser = client()
    assert browser.get("/badge", params={"tag": ""}).status_code == 400
    assert browser.get("/badge", params={"tag": "x" * 201}).status_code == 400
    assert browser.get("/badge").status_code == 422


def test_statistics_and_app_info():
    browser = client()
    browser.get("/badge", params={"tag": "stats"})
    assert browser.get("/api/stats/stats").json()["visit_count"] == 1
    assert browser.get("/api/stats/unknown").json()["visit_count"] == 0
    totals = {"total_tracked_tags": 1, "total_visits": 1, "new_badges_today": 1}
    assert browser.get("/api/stats").json() == totals
    assert set(browser.get("/api/app-info").json()) == {"environment", "version"}
    assert browser.get("/health").json()["status"] == "healthy"


def test_mediator_returns_a_new_visitor_id_only_for_new_visitors():
    mediator = build_mediator(temp_database())
    first = asyncio.run(mediator.send(RecordVisitCommand("t", "visits", "blue", "flat", "", None)))
    returning = RecordVisitCommand("t", "visits", "blue", "flat", "", first.new_visitor_id)
    again = asyncio.run(mediator.send(returning))
    assert first.new_visitor_id and again.new_visitor_id is None
    assert (first.visit_count, again.visit_count) == (1, 1)


def test_a_visitor_counts_on_every_badge_they_see():
    browser = client()
    browser.get("/badge", params={"tag": "first"})
    second = browser.get("/badge", params={"tag": "second"})
    assert count_in(second.headers["location"]) == "1"
    assert browser.get("/api/stats/second").json()["visit_count"] == 1


def test_legacy_databases_lose_the_per_visitor_unique_index():
    from src.infrastructure.persistence.peewee_visit_repository import PeeweeVisitRepository

    path = temp_database()
    legacy = PeeweeVisitRepository(path)
    legacy._database.execute_sql('CREATE UNIQUE INDEX "cookie_cookie_id" ON "cookie" ("cookie_id")')

    repository = PeeweeVisitRepository(path)
    assert repository.record_visit("first", "visitor") == 1
    assert repository.record_visit("second", "visitor") == 1
    assert repository.record_visit("second", "visitor") == 1


def test_sentry_stays_off_without_a_dsn_and_scrubs_cookies():
    from src.infrastructure.monitoring.sentry_error_reporter import SentryErrorReporter

    assert SentryErrorReporter(None, "test", "0.0.0").initialize() is False
    event = {
        "request": {
            "cookies": {"visitor_id": "abc"},
            "headers": {"Cookie": "visitor_id=abc", "Accept": "*/*"},
        }
    }
    scrubbed = SentryErrorReporter.scrub(event, {})
    assert scrubbed["request"]["cookies"] == "[Filtered]"
    assert scrubbed["request"]["headers"] == {"Cookie": "[Filtered]", "Accept": "*/*"}
