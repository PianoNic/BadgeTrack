# BadgeTrack Claude workflow rules

Never push to `main`. Every change goes:

1. **Issue**: open one (or pick existing) with at least one label from `gh label list`.
2. **Branch**: `feature/<issue#>_PascalCase` for new / refactor / docs, `fix/<issue#>_PascalCase` for bugs.
3. **PR**: short imperative title; body is one-line summary + `Closes #<issue>`; at least one label.
4. **Squash-merge + delete branch**, then `git fetch --prune && git reset --hard origin/main`.

## Branch naming

- ✅ `feature/15_PreactFrontend`
- ✅ `fix/18_CountVisitorsPerBadge`

## PR body

One line in commit-subject style, then `Closes #<issue>`. The commits already say what changed, so the PR doesn't need to repeat them.

```
Served badges directly so counts update instantly

Closes #26
```

## Commit subject

Past tense, verb first, short: about 3–7 words, one idea, no body. No "and … and …" lists, no file paths. Squash merges end with `(#PR)`.

- `Added <thing>`
- `Fixed <thing>`
- `Rebuilt <thing>`
- `Removed <thing>`

Examples:

- `Rebuilt the frontend in Preact (#23)`
- `Fixed visitors counting on only one badge (#20)`
- `Hid the server header (#28)`

Release bumps (written by `release.yaml`): `Bumped application.properties to X for release [skip ci]`.

No AI attribution of any kind: no `Co-Authored-By:` trailers (Claude, Copilot or otherwise) and no "Generated with Claude Code" footers. Squash-merge with `--body ""` so GitHub doesn't append trailers from the PR's commits.

## Labels

Pick from `gh label list`. BadgeTrack's active set: `feature`, `enhancement`, `bug`, `refactor`. Release Drafter resolves the next version from them (`feature`/`enhancement` → minor, `bug`/`refactor` → patch, `breaking` → major).

## Project

Visitor counter badges. FastAPI backend (onion architecture, CQRS via mediatorx, class-based controllers via `src/api/controller.py`), peewee + SQLite in `data/visitors.db`, Preact frontend in `frontend/` served by FastAPI as a SPA.

- **Run**: `cd frontend && npm install && npm run build`, then `python asgi.py` (http://localhost:8000). Python 3.14.
- **Frontend dev**: `npm run dev` in `frontend/`; Vite proxies `/api` and `/badge` to port 8000.
- **Tests / lint**: `python -m pytest tests`, `ruff check . && ruff format --check .` (`src/api/controller.py` is vendored and excluded).
- **Docker**: `docker compose up` (multi-stage build: Node builds the SPA, Python serves it). Mount `./data` or the counts are lost.
- **Version**: `application.properties` (`APP_VERSION`, `APP_ENVIRONMENT`). Don't bump it by hand; publishing a release runs `.github/workflows/release.yaml`, which writes the tag into it on main and then builds the image.
- **`/badge` is embedded in other people's READMEs**: its query parameters, the `visitor_id` cookie and the database schema must stay backwards compatible. It serves the shields.io SVG itself with caching off (shields.io caches for 5 days) and falls back to a redirect if shields.io is unreachable.
- **Errors**: set `SENTRY_DSN` to report 5xx errors to Sentry/GlitchTip.
- **Docs**: detail lives in `docs/` (self-hosting, configuration, API, development, architecture, releasing). Keep the README to screenshots, features, quick start and links; update the matching doc when behaviour changes.
