"""Starlette app for remote hosting of the Atla MCP Server."""

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount

from src.atla_mcp_server.server import mcp

# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#mounting-to-an-existing-asgi-server
app = Starlette(routes=[Mount("/", app=mcp.sse_app())])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
