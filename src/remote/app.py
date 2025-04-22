from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from mcp.server.fastmcp import FastMCP, Context
from starlette.middleware.base import RequestResponseEndpoint
import contextvars
from typing import Optional
import logging

mcp = FastMCP("Atla", debug=True)

_bearer_token: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "bearer_token", default=None
)


class BearerCaptureMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        header = request.headers.get("Authorization")
        if header:  # keep the whole string "Bearer xxxx"
            _bearer_token.set(header)
        return await call_next(request)


@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    token = _bearer_token.get()
    # await ctx.info(f"Token: {token}")  # Comment out or remove this
    logging.info(f"Token: {token}")  # Use standard logging instead

    return a + b


# mcp.tool()(evaluate_llm_response)


async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


app = Starlette(
    routes=[
        Route("/health", health_check),
        Mount("/", app=mcp.sse_app()),
    ],
)

app.add_middleware(BearerCaptureMiddleware)
