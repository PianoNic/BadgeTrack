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
  <a href="docs/self-hosting.md"><img src="https://img.shields.io/badge/Selfhost-Instructions-c8246b.svg" alt="Self-hosting"/></a>
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

## Quick start

Create a badge at [badgetrack.pianonic.ch](https://badgetrack.pianonic.ch), or write the URL yourself:

```markdown
![visits](https://badgetrack.pianonic.ch/badge?tag=my-project)
```

## Documentation

- [Badge URL and API](docs/api.md): every parameter and the stats endpoints
- [Self-hosting](docs/self-hosting.md): Docker Compose, data volume and updating
- [Configuration](docs/configuration.md): environment variables
- [Development](docs/development.md): running from source, tests and linting
- [Architecture](docs/architecture.md): how the code is organised
- [Releasing](docs/releasing.md): how versions and images are published

## License

[MIT](LICENSE)
