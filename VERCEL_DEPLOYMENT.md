# Deploying Archi VR API to Vercel

This note documents the steps taken to make this FastAPI project deployable
on Vercel using its Python runtime, and how to ship it with `vercel --prod`.

## 1. Fix `requirements.txt`

The existing `requirements.txt` had been generated with `pip freeze` against
a system Python environment, so it was full of unrelated OS packages
(`aptdaemon`, `PyGObject`, `dbus-python`, etc.) instead of this project's
actual dependencies.

Regenerated it from the project's `uv.lock` so it only lists real
dependencies:

```bash
uv export --no-hashes --no-dev -o requirements.txt
```

> Note: Vercel's builder actually prefers `uv.lock` when present and will use
> it directly. Keeping `requirements.txt` accurate still matters for local
> tooling, CI, and any environment that doesn't use `uv`.

## 2. Create a Python entrypoint for Vercel

Vercel's Python runtime looks for a top-level `app` variable (ASGI/WSGI) in a
recognized entrypoint file. Created `api/index.py`:

```python
"""Vercel serverless entrypoint."""

from app.app import app  # noqa: F401
```

This simply re-exports the existing FastAPI instance from `app/app.py` — no
application code needed to change.

## 3. Add `vercel.json`

Added a rewrite rule so every incoming path is routed to the single Python
function, letting FastAPI's own router (e.g. the `/api/v1` prefix) handle
path matching internally:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/api/index.py" }
  ]
}
```

Initially tried setting an explicit `functions.runtime: "python3.12"`, but
Vercel rejected that value (`Function Runtimes must have a valid version`).
Vercel auto-detects the Python version instead from `.python-version`
(already set to `3.12` in this repo), so the `functions` block was removed.

## 4. Upgrade `uv`

Local `vercel build` failed with:

```
Error: Found uv 0.9.18 ..., but Vercel requires uv 0.9.25 or newer.
```

Fixed by upgrading uv:

```bash
uv self update
```

## 5. Verify the build locally

```bash
vercel build --yes
```

This produced a working `.vercel/output` with a single `index.func` function
and the expected filesystem rewrite routes — confirming the project builds
correctly before deploying. Build output is a local artifact and should not
be committed (`.vercel` is already in `.gitignore`).

## 6. Set environment variables

The app reads its config from environment variables (via `pydantic-settings`
/ `.env`), and `.env` is git-ignored and never uploaded to Vercel. Before
deploying, set the required variables in the Vercel project (dashboard →
Project → Settings → Environment Variables, or `vercel env add <name>`):

- `NODE_ENV` (`PROD` for production)
- `POSTGRES_DB_PROD_URL`
- `RESEND_API_KEY`
- `RESEND_FROM_EMAIL`
- `RESEND_TO_EMAIL`
- `APP_API_KEY`

Without these, the app raises at import time (`DBConfig.get_db_url()` raises
`ValueError` if no DB URL is configured for the active environment).

## 7. Deploy

```bash
vercel --prod
```

## Known caveat

The FastAPI `lifespan` handler calls `init_db_and_tables()` on startup
(`Base.metadata.create_all`). Serverless cold starts don't guarantee the same
long-lived startup/shutdown lifecycle as a persistent server, so don't rely
on this to keep your schema in sync in production — use Alembic migrations
(`alembic upgrade head`) as the source of truth for schema changes instead.
