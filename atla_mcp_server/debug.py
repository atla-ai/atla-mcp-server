"""File for debugging the Atla MCP Server via the MCP Inspector."""

import os

from atla_mcp_server.server import app_factory

app = app_factory(atla_api_key=os.getenv("ATLA_API_KEY", ""))
