# Architecture

Onion architecture: dependencies point inwards only, and the API talks to the application exclusively through [mediatorx](https://pypi.org/project/mediatorx/) commands and queries.

```
src/
  domain/          badge request, badge styles, statistics, exceptions - no framework dependencies
  application/     use cases as commands and queries, plus the ports they need
    commands/      record_visit
    queries/       get_tag_statistics, get_system_statistics, get_application_info
    abstractions/  IVisitRepository, IBadgeUrlBuilder, IBadgeImageFetcher, IApplicationInfoProvider
  infrastructure/  peewee repository, shields.io adapters, configuration, Sentry, composition root
  api/             class-based FastAPI controllers that build a message and send it
frontend/          Preact SPA; npm run build emits frontend/dist, served at /
```

- **Controllers** use `@controller(router)` from `src/api/controller.py`, with the mediator as a shared class-level dependency.
- **`build_mediator()`** in `src/infrastructure/dependency_injection.py` is the one place that wires handlers to implementations.
- **Visits** are stored with peewee in SQLite: a `badge` row per tag with its count, and a `cookie` row per visitor and badge, unique on the pair.
- **Badge images** are built as shields.io URLs, fetched with httpx, cached in memory by URL and served with caching off.
- **The frontend** is Preact with Lucide icons. Its previews load shields.io directly and read counts from `/api/stats/{tag}`, so they never count a visit. FastAPI serves it with a SPA fallback: unknown paths return `index.html`, backend paths still 404.
