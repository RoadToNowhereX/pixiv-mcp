"""
Pixiv MCP Server - stdio transport
标准 MCP stdio 服务器入口，供 AstrBot 等客户端通过 stdin/stdout 调用
"""

import sys
import json
import asyncio
from pathlib import Path

# 将 src 目录加入 Python 路径，以便复用已有的 tools / auth 模块
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from tools import TOOLS, dispatch
from auth import ensure_refresh_token


server = Server("pixiv-mcp")


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict | None):
    arguments = arguments or {}
    result = await dispatch(name, arguments)
    return [
        TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2),
        )
    ]


def main():
    ensure_refresh_token()
    asyncio.run(run())


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    main()
