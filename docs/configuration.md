# Configuration

All settings are optional environment variables.

| Variable | Default | Description |
|---|---|---|
| `SENTRY_DSN` | not set | Reports server errors (5xx and `ERROR` logs) to Sentry or GlitchTip. The visitor cookie is scrubbed. |
| `LOG_LEVEL` | `INFO` | Python log level. |
| `APP_VERSION` | from `application.properties` | Overrides the version shown in the footer. Normally left unset; releases write it. |
| `APP_ENVIRONMENT` | from `application.properties` | Overrides the environment shown in the footer (`production` in release images). |

Older setups may still set `APP_ENV`, `SECRET_KEY` or `RATE_LIMIT_WINDOW_SECONDS`. Nothing reads them any more, so they can be removed.
