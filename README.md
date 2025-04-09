# Atla MCP Server
An MCP server implementation that provides a standardized interface for LLMs to interact with the Atla SDK and use our [state-of-the-art evaluation models](https://www.atla-ai.com/post/selene-1).

## Features
- Evaluate individual responses with Selene 1
- Run batch evaluations with Selene 1
- List available evaluation metrics, create new ones or fetch them by name
  
## Installation
1. Fork the repository and clone it locally in some directory. This will define your `path/to/atla-mcp-server`
```shell
git clone https://github.com/yourusername/atla-mcp-server.git
cd atla-mcp-server
pwd
# /path/to/atla-mcp-server
```

2. Install `uv` on your system into `/path/to/uv` if you don't have it already - you can find instructions [here](https://docs.astral.sh/uv/getting-started/installation/). For instance on MacOS:
```shell
brew install uv
which uv
# /path/to/uv
```

3. Install requirements into a virtual environment
```shell
cd /path/to/atla-mcp-server
uv venv
uv sync
```

4. Add your `ATLA_API_KEY` into your environment - you can find yours [here](https://www.atla-ai.com/sign-in). For instance on MacOS:
```shell
export ATLA_API_KEY=<your-atla-api-key> >> ~/.zshrc
source ~/.zshrc
echo $ATLA_API_KEY
```
- If you are building with OpenAI agents, you will also need an `OPENAI_API_KEY` in your environment



## Usage
### Use with OpenAI Agents SDK
The atla-mcp-server can be used with OpenAI agents as follows:
```python
from agents import Agent
from agents.mcp import MCPServerStdio
import os
atla_api_key = os.environ.get("ATLA_API_KEY") # You can also manually set your ATLA_API_KEY here

async with MCPServerStdio(
        params={
            "command": "python",
            "args": ["/path/to/atla-mcp-server/atla-mcp-server.py"],
            "env": {"ATLA_API_KEY":atla_api_key}
        }
    ) as atla_mcp_server:
        # Create an agent with the Atla evaluation server
        agent = Agent(
            name="AssistantWithAtlaEval",
            instructions="""
            You are a helpful assistant. Your goal is to provide high-quality responses to user requests.
            You can use the Atla evaluation tool to improve your responses.
            """,
            mcp_servers=[atla_mcp_server], # You can equip any Agent with Atla's MCP server like this
            model="gpt-4o-mini"
        )
```

For an example, run the following from `/path/to/atla-mcp-server`:
```shell
uv run examples/agent_with_atla_eval.py "Write a one-line poem about the ocean. Evaluate it for cliche and improve it once using the feedback."
```
You can also try out the notebook version of this example in `examples/agent_notebook.ipynb`.

### Use with Claude Desktop
- Download Claude Desktop from [here](https://claude.ai/download) (this is a local server, and won’t work with claude.ai on web) 
- Click on Claude → Settings… → Developer → Edit Config
- Add the following to the `claude_desktop_config.json` file (ensure that you replace `<your-atla-api-key>` with your actual Atla API key):
```json
{
	"mcpServers": {
		"atla-mcp-server": {
			"command": "/path/to/uv",
			"args": [
			"--directory",
			"/path/to/atla-mcp-server",
			"run",
			"atla-mcp-server.py"
			],
			"env": {
			"ATLA_API_KEY": "<your-atla-api-key>"
			}
		}
	}
}
```
- When you restart Claude Desktop, you should see `atla-mcp-server` in the list of available MCP servers, and 5 tools available to Claude.
- Example prompt to Claude: `Write a poem, evaluate it with atla for helpfulness`


### Use with Cursor
- Add the following to your `.cursor/mcp.json`:
```json
{
	"mcpServers": {
		"atla-mcp-server": {
			"command": "/path/to/uv",
			"args": [
			"--directory",
			"/path/to/atla-mcp-server",
			"run",
			"atla-mcp-server.py"
			],
			"env": {
			"ATLA_API_KEY": "<your-atla-api-key>"
			}
		}
	}
}
```
