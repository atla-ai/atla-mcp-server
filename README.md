# Atla MCP Server

An MCP server implementation that provides a standardized interface for LLMs to interact with the Atla SDK and use our [state-of-the-art evaluation models](https://www.atla-ai.com/post/selene-1).

## Features

- Evaluate individual responses with Selene 1
- Run batch evaluations with Selene 1
- List available evaluation metrics, create new ones or fetch them by name

## Usage

> To use the MCP server, you will need an Atla API key. You can find your existing API key [here](https://www.atla-ai.com/sign-in) or create a new one [here](https://www.atla-ai.com/sign-up).

### Remote Usage

Atla provides a hosted MCP server that can be used by any MCP client. This means that you can use the MCP server without needing to clone the repository and run it locally.

#### Connecting to the Server

##### Claude Desktop

> For more details on configuring MCP servers in Claude Desktop, refer to the [official MCP quickstart guide](https://modelcontextprotocol.io/quickstart/user).

1. Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "atla-mcp-server": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://atla-mcp-server.onrender.com/sse",
        "--header",
        "Authorization: Bearer ${ATLA_API_KEY}"
      ],
      "env": {
        "ATLA_API_KEY": "<your-atla-api-key>"
      }
    }
  }
}
```

2. **Restart Claude Desktop** to apply the changes.

You should now see options from `atla-mcp-server` in the list of available MCP tools.

##### Cursor

> For more details on configuring MCP servers in Cursor, refer to the [official documentation](https://docs.cursor.com/context/model-context-protocol).

1. Add the following to your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "atla-mcp-server": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://atla-mcp-server.onrender.com/sse",
        "--header",
        "Authorization: Bearer ${ATLA_API_KEY}"
      ],
      "env": {
        "ATLA_API_KEY": "<your-atla-api-key>"
      }
    }
  }
}
```

You should now see `atla-mcp-server` in the list of available MCP servers.

##### OpenAI Agents SDK

> For more details on using the OpenAI Agents SDK with MCP servers, refer to the [official documentation](https://openai.github.io/openai-agents-python/).

1. Install the OpenAI Agents SDK:

```shell
pip install openai-agents
```

2. Use the OpenAI Agents SDK to connect to the server:

```python
import os

from agents import Agent
from agents.mcp import MCPServerStdio

async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["mcp-remote", "https://atla-mcp-server.onrender.com/sse", "--header", "Authorization: Bearer ${ATLA_API_KEY}"],
            "env": {"ATLA_API_KEY": os.environ.get("ATLA_API_KEY")}
        }
    ) as atla_mcp_server:
        # Create an agent with the Atla evaluation server
        agent = Agent(
            name="AssistantWithAtlaEval",
            instructions="""
            You are a helpful assistant. Your goal is to provide high-quality responses to user requests.
            You can use the Atla evaluation tool to improve your responses.
            """,
            mcp_servers=[atla_mcp_server],
            model="gpt-4o-mini"
        )
```

### Local Usage

Local hosting is the conventional way of interacting with MCP servers. Running the server locally also allows you to extend functionality by adding new tools and resources.

#### Installation

> We recommend using [`uv`](https://docs.astral.sh/uv/) to manage the Python environment.

1. Clone the repository:

```shell
git clone https://github.com/yourusername/atla-mcp-server.git
cd atla-mcp-server
```

2. Create and activate a virtual environment:

```shell
uv venv
source .venv/bin/activate
```

3. Install dependencies depending on your needs:

```shell
# Basic installation
uv pip install -e .

# Installation with development tools (recommended)
uv pip install -e ".[dev]"
pre-commit install
```

4. Add your `ATLA_API_KEY` to your environment:

```shell
export ATLA_API_KEY=<your-atla-api-key>
```

#### Running the Server

After installation, you can run the server in several ways:

1. Using `uv run` (recommended):

```shell
uv run atla-mcp-server
```

2. Using Python directly:

```shell
python -m atla_mcp_server
```

3. From the repository root:

```shell
python src/atla_mcp_server/__main__.py
```

All methods will start the MCP server with `stdio` transport, ready to accept connections from MCP clients.

##### MCP Inspector

When developing locally, you can also [run the MCP Inspector](https://github.com/modelcontextprotocol/inspector) to test and debug the MCP server:

```shell
uv run mcp dev src/atla_mcp_server/__main__.py
```

#### Connecting to the Server

Once the server is running, you can connect to it using any MCP client.

##### Claude Desktop

Follow the instructions [above](#claude-desktop), but update your configuration file to use the local server:

```json
{
  "mcpServers": {
    "atla-mcp-server": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/atla-mcp-server",
        "run",
        "atla-mcp-server"
      ],
      "env": {
        "ATLA_API_KEY": "<your-atla-api-key>"
      }
    }
  }
}
```

##### Cursor

Follow the instructions [above](#cursor), but update your configuration file to use the local server:

```json
{
  "mcpServers": {
    "atla-mcp-server": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/atla-mcp-server",
        "run",
        "atla-mcp-server"
      ],
      "env": {
        "ATLA_API_KEY": "<your-atla-api-key>"
      }
    }
  }
}
```

##### OpenAI Agents SDK

Follow the instructions [above](#openai-agents-sdk), but update your configuration to use the local server:

```python
import os

from agents import Agent
from agents.mcp import MCPServerStdio

async with MCPServerStdio(
        params={
            "command": "uv",
            "args": ["run", "--directory", "/path/to/atla-mcp-server", "atla-mcp-server"],
            "env": {"ATLA_API_KEY": os.environ.get("ATLA_API_KEY")}
        }
    ) as atla_mcp_server:
    ...
```

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
