"""Entrypoint for the Atla MCP Server."""

from atla_mcp_server import mcp

if __name__ == "__main__":
    mcp.run(transport="stdio")
