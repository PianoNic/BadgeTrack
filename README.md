<p align="center">
  <img src="assets/logo.png" width="160" alt="BadgeTrack Logo">
</p>

<h1 align="center">BadgeTrack</h1>

<p align="center">
  <strong>Visitor counter badges for your READMEs and websites. Each browser counts once per badge.</strong>
</p>

<p align="center">
  <a href="https://github.com/PianoNic/BadgeTrack"><img src="https://badgetrack.pianonic.ch/badge?tag=badge-track&label=visits&color=c8246b&style=flat" alt="visits"/></a>
  <a href="https://github.com/PianoNic/BadgeTrack/blob/main/LICENSE"><img src="https://img.shields.io/github/license/PianoNic/BadgeTrack?color=c8246b&label=License" alt="License"/></a>
  <a href="https://github.com/PianoNic/BadgeTrack/releases"><img src="https://img.shields.io/github/v/release/PianoNic/BadgeTrack?include_prereleases&color=c8246b&label=Latest%20Release" alt="Latest release"/></a>
  <a href="https://badgetrack.pianonic.ch"><img src="https://img.shields.io/badge/Create%20Badge-badgetrack.pianonic.ch-c8246b.svg" alt="Create a badge"/></a>
  <a href="#installation"><img src="https://img.shields.io/badge/Selfhost-Instructions-c8246b.svg" alt="Self-hosting"/></a>
</p>

## Screenshots

<p align="center">
  <img src="assets/screenshots/home-light.png" width="49%" alt="Badge generator, light mode" />
  <img src="assets/screenshots/home-dark.png" width="49%" alt="Badge generator, dark mode" />
</p>

<details>
<summary><strong>Mobile</strong></summary>

<p align="center">
  <img src="assets/screenshots/mobile-dark.png" width="300" alt="Mobile view" />
</p>

</details>

## Features

- **Unique visitors**: each browser is counted once per badge, remembered by an anonymous cookie. Nothing else is stored.
- **Updates right away**: the badge image is served with caching turned off, so GitHub shows the new count on the next page load.
- **Any shields.io look**: every style (flat, flat square, plastic, for the badge, social), any colour and any [Simple Icons](https://simpleicons.org) logo.
- **Live preview**: the generator shows the real count and all five styles as you type, without counting a visit.
- **Self-hostable**: one container, one SQLite file.

## Usage

Create a badge at [badgetrack.pianonic.ch](https://badgetrack.pianonic.ch), or build the URL yourself:

```markdown
![visits](https://badgetrack.pianonic.ch/badge?tag=my-project&label=visits&color=c8246b&style=flat)
```

| Parameter | Default | Description |
|---|---|---|
| `tag` | required | Identifies the counter. Every embed with the same tag shares one count. |
| `label` | `visits` | Text on the left of the badge. |
| `color` | `4ade80` | Hex code or shields.io colour name. |
| `style` | `flat` | `flat`, `flat-square`, `plastic`, `for-the-badge` or `social`. |
| `logo` | none | A [Simple Icons](https://simpleicons.org) slug, e.g. `github`. |

`GET /api/stats/{tag}` returns a tag's count without counting a visit, and `GET /api/stats` returns the totals. Interactive docs live at `/docs`.

## Installation

### Docker Compose (recommended)

Create a `compose.yml`:

```yaml
services:
  badgetrack:
    image: pianonic/badgetrack:latest # Docker Hub
    # image: ghcr.io/pianonic/badgetrack:latest # GitHub Container Registry
    ports:
      - "8925:8000"
    volumes:
      - ./data:/app/data # the counts live here
    restart: unless-stopped
```

```bash
docker compose up -d
```

Open <http://localhost:8925>.

### Configuration

| Variable | Default | Description |
|---|---|---|
| `SENTRY_DSN` | not set | Reports server errors to Sentry or GlitchTip. |
| `LOG_LEVEL` | `INFO` | Python log level. |
| `APP_VERSION` / `APP_ENVIRONMENT` | from `application.properties` | Override the version and environment shown in the footer. |

### From source

Requires Python 3.14 and Node 22+.

```bash
cd frontend && npm install && npm run build && cd ..
pip install -r requirements.txt
python asgi.py
```

For frontend work, run `npm run dev` in `frontend/` next to `python asgi.py`; Vite proxies `/api` and `/badge` to port 8000.

Run the tests with `python -m pytest tests`.

<details>
<summary><strong>Tech stack</strong></summary>

- **Backend**: Python + FastAPI, peewee on SQLite, [mediatorx](https://pypi.org/project/mediatorx/) for CQRS, class-based controllers, optional Sentry.
- **Frontend**: [Preact](https://preactjs.com) + [Lucide](https://lucide.dev) icons, built with Vite and served by FastAPI as a SPA.
- **Architecture**: onion; dependencies point inwards only.

```
src/
  domain/          badge request, statistics, badge styles - no framework dependencies
  application/     record-visit command, statistics and app-info queries, plus the ports they need
  infrastructure/  peewee repository, shields.io adapters, configuration, Sentry, composition root
  api/             FastAPI controllers, which only build a message and send it
frontend/          Preact SPA; npm run build emits frontend/dist, served at /
```

</details>

## License

[MIT](LICENSE)
