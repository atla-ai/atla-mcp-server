# Atla MCP Server

An MCP server implementation providing a standardized interface for LLMs to interact with the Atla API for state-of-the-art LLMJ evaluation.

> Learn more about Atla [here](https://www.docs.atla-ai.com). Learn more about the Model Context Protocol [here](https://modelcontextprotocol.io).

<a href="https://glama.ai/mcp/servers/@atla-ai/atla-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@atla-ai/atla-mcp-server/badge" alt="Atla MCP server" />
</a>

## Available Tools

- `evaluate_llm_response`: Evaluate an LLM's response to a prompt using a given evaluation criteria. This function uses an Atla evaluation model under the hood to return a dictionary containing a score for the model's response and a textual critique containing feedback on the model's response.
- `evaluate_llm_response_on_multiple_criteria`: Evaluate an LLM's response to a prompt across _multiple_ evaluation criteria. This function uses an Atla evaluation model under the hood to return a list of dictionaries, each containing an evaluation score and critique for a given criteria.

## Usage

> To use the MCP server, you will need an Atla API key. You can find your existing API key [here](https://www.atla-ai.com/sign-in) or create a new one [here](https://www.atla-ai.com/sign-up).

### Installation

> We recommend using `uv` to manage the Python environment. See [here](https://docs.astral.sh/uv/getting-started/installation/) for installation instructions.

1. Clone the repository:

```shell
git clone https://github.com/atla-ai/atla-mcp-server.git
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
```

```shell
# Installation with development tools (recommended)
uv pip install -e ".[dev]"
pre-commit install
```

4. Add your `ATLA_API_KEY` to your environment:

```shell
export ATLA_API_KEY=<your-atla-api-key>
```

### Connecting to the Server

Once you have installed the server, you can connect to it using any MCP client.

Here, we provide specific instructions for connection to some common MCP clients.

> In what follows:
>
> - If you are having issues with `uv`, you might need to pass in the full path to the `uv` executable. You can find it by running `which uv` in your terminal.
> - `path/to/atla-mcp-server` is the path to the `atla-mcp-server` directory, which is the path to the repository you cloned in step 1.

> Having issues or need help connecting to another client? Feel free to open an issue or [contact us](mailto:support@atla-ai.com)!

#### OpenAI Agents SDK

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
            "command": "uv",
            "args": ["run", "--directory", "/path/to/atla-mcp-server", "atla-mcp-server"],
            "env": {"ATLA_API_KEY": os.environ.get("ATLA_API_KEY")}
        }
    ) as atla_mcp_server:
    ...
```

#### Claude Desktop

> For more details on configuring MCP servers in Claude Desktop, refer to the [official MCP quickstart guide](https://modelcontextprotocol.io/quickstart/user).

1. Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "atla-mcp-server": {
      "command": "uv",
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

2. **Restart Claude Desktop** to apply the changes.

You should now see options from `atla-mcp-server` in the list of available MCP tools.

#### Cursor

> For more details on configuring MCP servers in Cursor, refer to the [official documentation](https://docs.cursor.com/context/model-context-protocol).

1. Add the following to your `.cursor/mcp.json` file:

```json
{
  "mcpServers": {
    "atla-mcp-server": {
      "command": "uv",
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

You should now see `atla-mcp-server` in the list of available MCP servers.


### Running the Server

> If you are using an MCP client, you will generally not need to run the server locally.

Running the server locally can be useful for development and debugging. After installation, you can run the server in several ways:

1. Using `uv run` (recommended):

```shell
cd path/to/atla-mcp-server
uv run atla-mcp-server
```

2. Using Python directly:

```shell
cd path/to/atla-mcp-server
python -m atla_mcp_server
```

3. With the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```shell
cd path/to/atla-mcp-server
uv run mcp dev src/atla_mcp_server/debug.py
```

All methods will start the MCP server with `stdio` transport, ready to accept connections from MCP clients. The MCP Inspector will provide a web interface for testing and debugging the MCP server.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.