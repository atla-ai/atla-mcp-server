# Remote Hosting for Atla MCP Server

> Note: If you're not interested in remote hosting of your own MCP Server, you can ignore this directory!

This directory contains the code that supports the [official remote Atla MCP Server](TODO: ADD LINK TO MAIN README).

This code can also be run locally as a starting point for your own remote MCP Server implementation.

## Quickstart

1. Install with remote dependencies:

```shell
uv pip install -e ".[remote]"
```

2. Run locally:

```shell
uv run uvicorn remote.app:app
```
