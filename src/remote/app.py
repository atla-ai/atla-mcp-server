"""Starlette app for remote hosting of the Atla MCP Server.

See [here](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#mounting-to-an-existing-asgi-server)
for more details.
"""

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from atla_mcp_server.server import mcp


async def health_check():
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "status_code": 200})


app = Starlette(
    routes=[
        Route("/", health_check),  # Health check endpoint at root.
        Mount("/", app=mcp.sse_app()),  # Sets up /sse endpoint.
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
