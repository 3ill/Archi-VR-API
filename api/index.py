"""Vercel serverless entrypoint.

Vercel's Python runtime looks for an ASGI-compatible `app` object in this
module and wraps it automatically, so we simply re-export the FastAPI
instance defined in app.app.
"""

from app.app import app  # noqa: F401
