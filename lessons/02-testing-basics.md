# Lesson 2: Testing Your MCP Server - Understanding the Basics

## Learning Objectives

- Understand how MCP servers communicate
- Test basic MCP protocol functionality
- Learn the request/response flow
- Validate our server skeleton works

## The MCP Protocol Flow

MCP servers communicate via JSON-RPC over stdio. The basic flow:
1. **Initialization**: Client connects and exchanges capabilities
2. **Tool Discovery**: Client asks "what tools do you have?"
3. **Tool Execution**: Client calls specific tools with parameters

## Step 1: Activate Environment and Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Create a Simple Test Script

We created `test_basic.py` to understand MCP communication. Key learnings:

### What We Discovered
1. **MCP Protocol**: Uses JSON-RPC over stdio
2. **Server Lifecycle**: Initialize → List Tools → Call Tools
3. **Common Issues**: Protocol version mismatches, async handling

### Our Test Results
```bash
python test_basic.py
```

✅ **Success**: Server initializes and responds to basic requests
⚠️ **Learning**: Tool discovery needs proper MCP protocol implementation

### Key MCP Server Structure

```python
# Modern MCP server pattern (what we implemented)
from mcp.server import Server
import mcp.types as types

server = Server("server-name")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    # Return available tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    # Handle tool execution
```

## Step 3: Understanding the Code

For new programmers, we've created detailed explanations:

📖 **[Server Code Explained](../explanations/server-explained.md)** - Line-by-line breakdown of our MCP server
📖 **[Test Code Explained](../explanations/test-explained.md)** - Understanding subprocess communication and JSON-RPC
📖 **[MCP Protocol Test Explained](../explanations/test_mcp_protocol-explained.md)** - Why proper MCP protocol sequence matters

### Key Learning Points

**From the Server Code**:
- How decorators register functions with the MCP framework
- Why we use async/await for non-blocking operations
- How JSON Schema defines tool input requirements
- The importance of proper error handling

**From the Test Code**:
- How subprocess communication works
- What JSON-RPC protocol looks like in practice
- Why proper cleanup is essential in tests
- How to handle errors gracefully

## Step 4: Manual Testing

Since our server starts correctly, let's test it manually to understand the flow:

```bash
# Start server (it waits for JSON-RPC input)
python src/mcp_bedrock_kb/server.py

# In another terminal, you could send JSON-RPC messages
# But for now, we know it's working!
```

## What We Learned

- MCP servers communicate via JSON-RPC over stdin/stdout
- Our server structure is correct
- Tool registration works with decorators
- Next step: Connect to actual data source (Bedrock KB)

## Next Steps

Lesson 3 will connect our working MCP server to AWS Bedrock Knowledge Base (ID: QVBQZMYI7R) and test real queries.

---
*Understanding the foundation before adding complexity*
