# Badge URL and API

Interactive docs are served at `/docs`.

## `GET /badge`

Counts the visit and returns the badge as an SVG.

```markdown
![visits](https://badgetrack.pianonic.ch/badge?tag=my-project&label=visits&color=c8246b&style=flat)
```

| Parameter | Default | Description |
|---|---|---|
| `tag` | required | Identifies the counter, up to 200 characters. Every embed with the same tag shares one count. |
| `label` | `visits` | Text on the left of the badge, up to 20 characters. |
| `color` | `4ade80` | Hex code (with or without `#`) or a shields.io colour name. |
| `style` | `flat` | `flat`, `flat-square`, `plastic`, `for-the-badge` or `social`. Anything else falls back to `flat`. |
| `logo` | none | A [Simple Icons](https://simpleicons.org) slug, e.g. `github`. |

**Counting**: a new browser gets an anonymous `visitor_id` cookie and is counted once per tag. Seeing the same badge again does not count; seeing a different badge does.

**Caching**: the SVG is fetched from shields.io and served with `Cache-Control: max-age=0, no-cache, no-store`, so image proxies such as GitHub's show the new count on the next load. shields.io itself asks for 5 days of caching, which is why BadgeTrack does not simply redirect. If shields.io cannot be reached, `/badge` falls back to a redirect so the badge still renders.

An invalid `tag`, `label`, `color` or `logo` returns `400`.

## `GET /api/stats/{tag}`

Reads a tag's count without counting a visit. The web app uses it for the live preview.

```json
{ "tag": "my-project", "visit_count": 1284 }
```

## `GET /api/stats`

```json
{ "total_tracked_tags": 4, "total_visits": 1404 }
```

## `GET /api/app-info`

```json
{ "environment": "production", "version": "2.0.0" }
```
