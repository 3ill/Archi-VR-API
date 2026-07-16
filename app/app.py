from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.v1.router import api_router
from app.core.logger import setup_logging
from app.core.request_id_middleware import request_id_middleware
from app.core.security.api_key_dependency import verify_api_key
from app.db.db import init_db_and_tables
from app.shared.event.event_subscriber import EventSubscribers

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_and_tables()
    print("Database initialized successfully")

    EventSubscribers()
    print("Event subscription active")
    yield


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://polaroid-visualizer.vercel.app",
    "https://archivr-visualizer.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(request_id_middleware)

app.include_router(api_router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Archi VR API",
        version="1.0.0",
        description="API documentation for Archi VR",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "name": "x-api-key",
            "in": "header",
        },
        "SecurityKeyAuth": {
            "type": "apiKey",
            "name": "x-security-key",
            "in": "header",
        },
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "admin" in method.get("tags", []):
                method["security"] = [{"BearerAuth": []}, {"SecurityKeyAuth": []}]
            else:
                method["security"] = [{"BearerAuth": []}, {"ApiKeyAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
