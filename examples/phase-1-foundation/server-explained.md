# MCP Server Code Explanation - Line by Line

This document explains every line of our MCP server code for new programmers. We'll cover the "why" behind each decision.

## File: `src/mcp_bedrock_kb/server.py`

### The Shebang and Docstring

```python
#!/usr/bin/env python3
```
**What**: This is called a "shebang" - it tells the operating system which interpreter to use when running this file directly.
**Why**: Allows us to run `./server.py` instead of `python server.py`. The `env` command finds Python3 wherever it's installed.

```python
"""
MCP Bedrock Knowledge Base Server

A minimal MCP server that connects to AWS Bedrock Knowledge Base
to provide enhanced documentation queries.
"""
```
**What**: A docstring - Python's way of documenting what a module/function does.
**Why**: Good documentation helps other developers (and future you) understand the purpose. Triple quotes allow multi-line strings.

### Imports - Bringing in External Code

```python
import asyncio
```
**What**: Python's built-in library for asynchronous programming.
**Why**: MCP servers need to handle multiple requests without blocking. `asyncio` lets us write code that can pause and resume, allowing other tasks to run.

```python
from mcp.server.models import InitializationOptions
```
**What**: Imports a specific class from the MCP library.
**Why**: `InitializationOptions` tells the MCP client what our server can do. We import only what we need to keep our code clean.

```python
import mcp.types as types
```
**What**: Imports the MCP types module and gives it a shorter name.
**Why**: MCP has specific data types (like `Tool`, `TextContent`). The `as types` makes our code more readable: `types.Tool` instead of `mcp.types.Tool`.

```python
from mcp.server import NotificationOptions, Server
```
**What**: Imports the main Server class and notification settings.
**Why**: `Server` is the core of our MCP server. `NotificationOptions` configures how our server communicates with clients.

```python
import boto3
```
**What**: AWS SDK for Python.
**Why**: We'll use this to connect to AWS Bedrock Knowledge Base. Even though we're not using it yet, we import it now so it's ready.

### Creating the Server Instance

```python
server = Server("bedrock-kb")
```
**What**: Creates a new MCP server with the name "bedrock-kb".
**Why**: This is our server's identity. Clients will see this name when they connect. The name should be descriptive and unique.

### Tool Discovery - What Can Our Server Do?

```python
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
```
**What**: A decorator that registers this function to handle "list tools" requests.
**Why**: When a client (like Q CLI) connects, it asks "what tools do you have?" This function answers that question.

**Breaking down the syntax**:
- `@server.list_tools()`: Decorator - tells the server "call this function when someone asks for tools"
- `async def`: Asynchronous function - can pause and resume without blocking
- `-> list[types.Tool]`: Type hint - tells other developers this returns a list of Tool objects

```python
"""Return available tools"""
```
**What**: Function docstring.
**Why**: Documents what this specific function does.

```python
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
```
**What**: Returns a list containing one Tool object.
**Why**: This defines what our tool does and what input it expects.

**Breaking down the Tool**:
- `name`: Unique identifier for the tool
- `description`: Human-readable explanation of what it does
- `inputSchema`: JSON Schema defining expected input format
  - `"type": "object"`: Input should be a dictionary/object
  - `"properties"`: Defines what fields the object can have
  - `"required"`: Lists which fields must be provided

### Tool Execution - Actually Doing the Work

```python
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
```
**What**: Decorator that registers this function to handle tool execution requests.
**Why**: When a client wants to use a tool, this function gets called.

**Parameter explanation**:
- `name: str`: Which tool the client wants to use
- `arguments: dict | None`: The input data (could be None if no arguments)
- `-> list[types.TextContent]`: Returns a list of text responses

```python
"""Handle tool calls"""
```
**What**: Function docstring.

```python
if name == "query_strands_docs":
    query = arguments.get("query", "") if arguments else ""
    return await query_knowledge_base(query)
else:
    raise ValueError(f"Unknown tool: {name}")
```
**What**: Checks which tool was requested and calls the appropriate function.
**Why**: Our server might have multiple tools. We need to route the request to the right handler.

**Breaking down the logic**:
- `if name == "query_strands_docs"`: Check if this is our documentation query tool
- `arguments.get("query", "")`: Safely get the "query" field, default to empty string if missing
- `if arguments else ""`: Handle case where arguments is None
- `await query_knowledge_base(query)`: Call our query function (await because it's async)
- `raise ValueError(...)`: If unknown tool requested, throw an error

### The Actual Query Function

```python
async def query_knowledge_base(query: str) -> list[types.TextContent]:
```
**What**: Function that will query our Bedrock Knowledge Base.
**Why**: Separating this logic makes our code more organized and testable.

```python
"""Query the Bedrock Knowledge Base"""
```
**What**: Function docstring.

```python
# TODO: We'll implement this in the next lesson
return [types.TextContent(
    type="text",
    text=f"Placeholder response for query: {query}\n\nThis will connect to Bedrock Knowledge Base (ID: QVBQZMYI7R) in the next lesson."
)]
```
**What**: Placeholder implementation that returns fake data.
**Why**: This lets us test our server structure before adding AWS complexity. The `f"..."` is an f-string for string formatting.

### Starting the Server

```python
async def main():
```
**What**: Main entry point function.
**Why**: Good practice to have a main function rather than running code at module level.

```python
"""Main entry point"""
```
**What**: Function docstring.

```python
from mcp.server.stdio import stdio_server
```
**What**: Import inside function to avoid event loop issues.
**Why**: Some imports need to happen after asyncio is set up. Importing here prevents timing problems.

```python
async with stdio_server() as (read_stream, write_stream):
```
**What**: Creates input/output streams for communication.
**Why**: MCP servers communicate via stdin/stdout. This sets up those communication channels.

**Breaking down the syntax**:
- `async with`: Asynchronous context manager - automatically cleans up when done
- `stdio_server()`: Creates standard input/output server
- `as (read_stream, write_stream)`: Unpacks the returned streams into two variables

```python
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
```
**What**: Starts the server with configuration options.
**Why**: This is where our server actually begins listening for requests.

**Breaking down the configuration**:
- `read_stream, write_stream`: How the server communicates
- `server_name`: Identity of our server
- `server_version`: Version number for compatibility
- `capabilities`: What features our server supports
- `notification_options`: How to handle notifications
- `experimental_capabilities`: Future features (empty for now)

### Script Entry Point

```python
if __name__ == "__main__":
    asyncio.run(main())
```
**What**: Only runs if this file is executed directly (not imported).
**Why**: Allows our file to be both a runnable script and an importable module.

**Breaking it down**:
- `if __name__ == "__main__"`: Python idiom - only true when file is run directly
- `asyncio.run(main())`: Starts the async event loop and runs our main function

## Key Concepts for New Programmers

1. **Async/Await**: Allows code to pause and resume, enabling multiple operations simultaneously
2. **Decorators (@)**: Modify or register functions without changing their code
3. **Type Hints**: Help other developers understand what data types functions expect
4. **Context Managers (with)**: Automatically handle setup and cleanup
5. **JSON Schema**: Standard way to describe data structure requirements

## Why This Structure?

- **Separation of Concerns**: Each function has one job
- **Error Handling**: Clear error messages when things go wrong
- **Extensibility**: Easy to add more tools later
- **Standards Compliance**: Follows MCP protocol exactly
- **Testability**: Each piece can be tested independently
