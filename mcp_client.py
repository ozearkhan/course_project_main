import anyio
import json

from langsmith import traceable
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys

SERVER = StdioServerParameters(
    command=sys.executable,
    args=["-m", "mcp_server.server"],
)


class MCPClient:

    async def call_tool(self, tool_name: str, arguments: dict):

        async with stdio_client(SERVER) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(
                    tool_name,
                    arguments,
                )
                content = result.content

                if not content:
                    return None

                text = content[0].text

                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return text



client = MCPClient()

@traceable(run_type="tool")
def call_tool(tool_name: str, arguments: dict):
    return anyio.run(
        client.call_tool,
        tool_name,
        arguments,
    )