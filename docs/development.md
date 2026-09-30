# Development

Python 3.14 and Node 24 are what CI and the Docker image use.

## Run from source

```bash
cd frontend && npm install && npm run build && cd ..
pip install -r requirements.txt
python asgi.py
```

The app runs on <http://localhost:8000>, stores its database in `data/visitors.db` and serves the built frontend from `frontend/dist`.

## Frontend with hot reload

```bash
python asgi.py            # backend on :8000
cd frontend && npm run dev # frontend on :5173, proxies /api and /badge to :8000
```

## Tests and linting

```bash
pip install pytest ruff
python -m pytest tests
ruff check . && ruff format --check .
```

The tests never call shields.io; without an image `/badge` falls back to its redirect, which is what most tests assert on. `src/api/controller.py` is vendored from fastapi-utils via SchulwareAPI and excluded from linting so it can be re-synced unchanged.

## Contributing

Every change goes through an issue, a `feature/<issue>_Name` or `fix/<issue>_Name` branch and a labelled PR that is squash-merged. The full rules live in [`.claude/CLAUDE.md`](../.claude/CLAUDE.md).
