# Self-hosting

BadgeTrack is one container with one SQLite database.

## Docker Compose (recommended)

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

**Keep the `./data` volume.** The counts are stored in `data/visitors.db`; without the volume they are lost when the container is recreated. Databases from older versions are migrated automatically on startup.

## Behind a reverse proxy

The app uses relative URLs, so it works on its own domain or under a sub-path. Badges embed the absolute URL of the page they were created on, so create them on the public address, not on `localhost`.

## Updating

```bash
docker compose pull && docker compose up -d
```

Images are tagged `latest`, `X`, `X.Y` and `X.Y.Z`. See [Configuration](configuration.md) for environment variables.
