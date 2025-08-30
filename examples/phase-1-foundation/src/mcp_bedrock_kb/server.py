#!/usr/bin/env python3
"""
MCP Bedrock Knowledge Base Server

A minimal MCP server that connects to AWS Bedrock Knowledge Base
to provide enhanced documentation queries.
"""

import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import boto3


# Create server instance
server = Server("bedrock-kb")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Return available tools"""
    return [
        types.Tool(
            name="query_strands_docs",
            description="Query AWS Strands Agent documentation using Bedrock Knowledge Base",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The question or topic to search for in the documentation"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls"""
    if name == "query_strands_docs":
        query = arguments.get("query", "") if arguments else ""
        return await query_knowledge_base(query)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def query_knowledge_base(query: str) -> list[types.TextContent]:
    """Query the Bedrock Knowledge Base"""
    # TODO: We'll implement this in the next lesson
    return [types.TextContent(
        type="text",
        text=f"Placeholder response for query: {query}\n\nThis will connect to Bedrock Knowledge Base (ID: QVBQZMYI7R) in the next lesson."
    )]

async def main():
    """Main entry point"""
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="bedrock-kb",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
