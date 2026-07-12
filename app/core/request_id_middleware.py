import uuid

from fastapi import Request

from app.core.request_context import request_id_ctx_var


async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    request_id_ctx_var.set(request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response
