"""Starlette app for remote hosting of the Atla MCP Server.

See [here](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#mounting-to-an-existing-asgi-server)
for more details.
"""

from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from atla_mcp_server.server import mcp

app = mcp.sse_app()
sse = SseServerTransport("/messages")


async def handle_sse(scope, receive, send):
    """Handle SSE connections."""
    async with sse.connect_sse(scope, receive, send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


async def handle_messages(scope, receive, send):
    """Handle messages sent to the server."""
    await sse.handle_post_message(scope, receive, send)


async def health_check(request: Request):
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "status_code": 200})


app = Starlette(
    routes=[
        Route("/", health_check),  # Health check endpoint at root.
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ]
)
