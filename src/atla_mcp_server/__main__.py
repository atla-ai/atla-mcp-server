"""Entrypoint for the Atla MCP Server."""

from atla_mcp_server.server import mcp


def main():
    """Run the Atla MCP Server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
