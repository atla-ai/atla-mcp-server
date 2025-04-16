"""Entrypoint for the Atla MCP Server."""

import argparse
import os

from atla_mcp_server.server import app_factory


def main():
    """Entrypoint for the Atla MCP Server."""
    print("Starting Atla MCP Server with stdio transport...")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--atla-api-key",
        type=str,
        required=False,
        help="Atla API key. Can also be set via ATLA_API_KEY environment variable.",
    )
    args = parser.parse_args()

    if args.atla_api_key:
        print("Using Atla API key from --atla-api-key CLI argument...")
        atla_api_key = args.atla_api_key
    elif os.getenv("ATLA_API_KEY"):
        atla_api_key = os.getenv("ATLA_API_KEY")
        print("Using Atla API key from ATLA_API_KEY environment variable...")
    else:
        parser.error(
            "Atla API key must be provided either via --atla-api-key argument "
            "or ATLA_API_KEY environment variable"
        )

    print("Creating server...")
    app = app_factory(atla_api_key)

    print("Running server...")
    app.run(transport="stdio")


if __name__ == "__main__":
    main()
