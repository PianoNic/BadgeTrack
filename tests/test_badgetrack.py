import asyncio
import os
import sys
import tempfile
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from src.api.app import create_app
from src.application.commands.record_visit.record_visit_command import RecordVisitCommand
from src.infrastructure.badges.shields_badge_image_fetcher import ShieldsBadgeImageFetcher
from src.infrastructure.dependency_injection import build_mediator

original_fetch = ShieldsBadgeImageFetcher.fetch


async def _no_network(_self, _url):
    return None


# tests never call shields.io; without an image /badge falls back to redirecting there
ShieldsBadgeImageFetcher.fetch = _no_network


def temp_database() -> str:
    # a file, not ":memory:": peewee opens one connection per thread and the test client serves on another
    return os.path.join(tempfile.mkdtemp(), "visitors.db")


def client() -> TestClient:
    return TestClient(create_app(temp_database()), follow_redirects=False)


def count_in(location: str) -> str:
    return urlparse(location).path.split("/")[-1].split("-")[1]


def test_badge_falls_back_to_a_shields_redirect_and_sets_a_visitor_cookie():
    response = client().get("/badge", params={"tag": "readme", "color": "237e61", "logo": "github"})
    assert response.status_code == 302
    location = response.headers["location"]
    assert location.startswith("https://img.shields.io/badge/visits-1-237e61.svg")
    assert parse_qs(urlparse(location).query) == {"style": ["flat"], "logo": ["github"]}
    assert "no-store" in response.headers["cache-control"]
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
    assert browser.get("/api/stats").json() == {"total_tracked_tags": 1, "total_visits": 1}
    assert set(browser.get("/api/app-info").json()) == {"environment", "version"}


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


def test_every_shields_style_and_awkward_labels_render():
    browser = client()
    for style in ("flat", "flat-square", "plastic", "for-the-badge", "social"):
        location = browser.get("/badge", params={"tag": "styles", "style": style}).headers["location"]
        assert parse_qs(urlparse(location).query)["style"] == [style]
    fallback = browser.get("/badge", params={"tag": "styles", "style": "nonsense"}).headers["location"]
    assert parse_qs(urlparse(fallback).query)["style"] == ["flat"]

    location = browser.get(
        "/badge", params={"tag": "t", "label": "page_views-x", "color": "#C8246B"}
    ).headers["location"]
    assert urlparse(location).path == "/badge/page__views--x-1-C8246B.svg"


def test_spa_fallback_serves_index_but_keeps_backend_404s():
    import tempfile
    from pathlib import Path

    from fastapi import FastAPI

    from src.api.app import SpaStaticFiles

    dist = Path(tempfile.mkdtemp())
    (dist / "index.html").write_text("<p>spa</p>")
    app = FastAPI()
    app.mount("/", SpaStaticFiles(directory=dist, html=True))
    browser = TestClient(app)

    assert browser.get("/").text == "<p>spa</p>"
    assert browser.get("/about").text == "<p>spa</p>"
    assert browser.get("/api/nope").status_code == 404


def test_badge_svg_is_served_directly_with_caching_off():
    async def fake_shields(_self, url):
        return f"<svg>{url}</svg>".encode()

    ShieldsBadgeImageFetcher.fetch = fake_shields
    try:
        response = client().get("/badge", params={"tag": "fresh"})
    finally:
        ShieldsBadgeImageFetcher.fetch = _no_network

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert "no-store" in response.headers["cache-control"]
    assert response.headers["content-security-policy"].startswith("default-src 'none'")
    assert "visits-1-" in response.text
    assert "visitor_id=" in response.headers["set-cookie"]


def test_fetched_badges_are_cached_by_url():
    import httpx

    calls = []

    def shields(request):
        calls.append(str(request.url))
        return httpx.Response(200, headers={"content-type": "image/svg+xml"}, content=b"<svg/>")

    fetcher = ShieldsBadgeImageFetcher(cache_size=1)
    fetcher._client = httpx.AsyncClient(transport=httpx.MockTransport(shields))
    fetch = original_fetch.__get__(fetcher)

    for url in ("a", "a", "b", "a"):
        assert asyncio.run(fetch(f"https://img.shields.io/{url}.svg")) == b"<svg/>"
    assert [call[-5:] for call in calls] == ["a.svg", "b.svg", "a.svg"]
