import os
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import json
import argparse 

async def main(user_request):
    # Create MCP Server for Atla Evaluation
    async with MCPServerStdio(
        params={
            "command": "python",
            "args": ["atla-mcp-server.py"],
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
            mcp_servers=[atla_mcp_server], # You can equip any Agent with Atla's MCP server like this
            model="gpt-4o-mini"
        )
                
        # Run the agent
        result = await Runner.run(agent, user_request)

       # Print the agent's internal steps
        for item in result.new_items:
            if item.type == "message_output_item":
                print("\n*******  Agent's response: ******")
                print(item.raw_item.content[0].text)
            elif item.type == 'tool_call_item':
                print("\n*******  Agent's request to Atla tool: ******:")
                print(json.loads(item.raw_item.arguments))
            elif item.type == 'tool_call_output_item':
                print("\n*******  Atla's response to Agent's request: ******:")
                print(json.loads(json.loads(item.output)['text']))

if __name__ == "__main__":
    # Check if API keys are set
    if not os.environ.get("ATLA_API_KEY"):
        raise ValueError("Please set the ATLA_API_KEY environment variable.")
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
        
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the agent with Atla evaluation.")
    parser.add_argument("user_request", type=str, help="The user request to process.")
    args = parser.parse_args()
    user_request = args.user_request
    
    # Run the main function
    asyncio.run(main(user_request))