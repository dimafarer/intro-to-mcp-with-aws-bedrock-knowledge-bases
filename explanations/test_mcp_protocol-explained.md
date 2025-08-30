# MCP Protocol Test Explanation - Line by Line

This document explains why our original test failed with AWS integration and how the proper MCP protocol test works.

## Why the Original Test Failed

### The Problem with `test_basic.py`
Our original test worked for Phase 1 but failed with AWS integration because:

1. **Missing Initialization Sequence**: MCP protocol requires proper initialization before any operations
2. **No Initialized Notification**: After initialization, clients must send an "initialized" notification
3. **Protocol Violations**: Skipping steps causes "Invalid request parameters" errors

### The Error We Saw
```
{"jsonrpc":"2.0","id":2,"error":{"code":-32602,"message":"Invalid request parameters","data":""}}
```

**Why This Happened**: We tried to call tools before completing the MCP handshake sequence.

## File: `tests/test_mcp_protocol.py`

### Imports and Setup

```python
#!/usr/bin/env python3
"""
Proper MCP protocol test following initialization sequence
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
```
**What**: Same imports as before, but now we'll use them correctly.
**Why**: We need these tools to communicate with our MCP server process.

### The Proper MCP Protocol Sequence

```python
async def test_mcp_protocol():
    """Test MCP server following proper protocol sequence"""
    
    print("🔄 Testing MCP Protocol Sequence")
    print("=" * 40)
```
**What**: Main test function with clear output.
**Why**: Good tests tell you what they're doing.

### Server Process Setup

```python
server_path = Path(__file__).parent / "src" / "mcp_bedrock_kb" / "server.py"

try:
    process = subprocess.Popen(
        [sys.executable, str(server_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
```
**What**: Same server startup as before.
**Why**: We still need to run our server as a separate process.

**Note**: The path is different because we're now in `tests/` directory, so we need to go up one level to find `src/`.

### Step 1: Proper Initialization

```python
print("1. Initializing...")
init_msg = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1.0"}
    }
}

process.stdin.write(json.dumps(init_msg) + "\n")
process.stdin.flush()

init_response = process.stdout.readline()
print(f"   Response: {init_response.strip()}")
```
**What**: Send initialization request and read response.
**Why**: MCP servers must be initialized before they accept any other requests.

**Key Points**:
- `"method": "initialize"`: This is the required first step
- `"protocolVersion"`: Must match what the server supports
- We read and display the response to verify it worked

### Step 2: The Critical Missing Piece

```python
print("2. Sending initialized notification...")
initialized_msg = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized",
    "params": {}
}

process.stdin.write(json.dumps(initialized_msg) + "\n")
process.stdin.flush()
```
**What**: Send the "initialized" notification.
**Why**: This is what our original test was missing! After initialization, clients must notify the server they're ready.

**Critical Differences**:
- **No `"id"` field**: Notifications don't have IDs (they don't expect responses)
- `"method": "notifications/initialized"`: Specific notification type
- **No response expected**: We don't read stdout after this

### Step 3: Now We Can List Tools

```python
print("3. Listing tools...")
tools_msg = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
}

process.stdin.write(json.dumps(tools_msg) + "\n")
process.stdin.flush()

tools_response = process.stdout.readline()
print(f"   Response: {tools_response.strip()}")
```
**What**: Request available tools (same as before).
**Why**: Now that initialization is complete, the server will respond properly.

**What We'll See**: The server will return our `query_strands_docs` tool with its description and input schema.

### Step 4: Call the Tool with Real AWS Query

```python
print("4. Calling tool...")
call_msg = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "query_strands_docs",
        "arguments": {"query": "What is AWS Strands?"}
    }
}

process.stdin.write(json.dumps(call_msg) + "\n")
process.stdin.flush()

call_response = process.stdout.readline()
print(f"   Response: {call_response.strip()}")
```
**What**: Execute our tool with a real query.
**Why**: This tests the complete flow: MCP protocol → AWS Bedrock → formatted response.

**What Happens**:
1. Server receives the tool call
2. Extracts the query "What is AWS Strands?"
3. Calls AWS Bedrock Knowledge Base
4. Formats the response with Query, Answer, and Sources
5. Returns it as MCP TextContent

### Cleanup

```python
print("\n✅ MCP protocol test completed!")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'process' in locals():
        process.terminate()
        process.wait()
```
**What**: Same cleanup pattern as before.
**Why**: Always clean up processes, even if errors occur.

## The Complete MCP Protocol Flow

### What Our Test Demonstrates

1. **Client → Server**: `initialize` request
2. **Server → Client**: Initialization response with capabilities
3. **Client → Server**: `notifications/initialized` (no response expected)
4. **Client → Server**: `tools/list` request
5. **Server → Client**: List of available tools
6. **Client → Server**: `tools/call` request
7. **Server → Client**: Tool execution result

### Why This Sequence Matters

- **Security**: Servers can validate client capabilities before accepting requests
- **Capability Negotiation**: Client and server agree on what features to use
- **State Management**: Server knows when client is ready to receive requests
- **Error Prevention**: Prevents protocol violations that cause cryptic errors

## Key Differences from Original Test

### What Was Wrong Before
```python
# OLD - This fails after AWS integration
tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
# Sent immediately after init - WRONG!
```

### What's Right Now
```python
# NEW - Proper sequence
init_msg = {...}  # Step 1: Initialize
initialized_msg = {...}  # Step 2: Send initialized notification  
tools_msg = {...}  # Step 3: Now we can list tools
```

## Why It Worked in Phase 1 But Not Phase 2

**Phase 1**: Our server was simpler and more forgiving of protocol violations
**Phase 2**: AWS integration made the server more strict about MCP protocol compliance

**The Real Issue**: We were never following MCP protocol correctly, but it didn't matter until we had real functionality to protect.

## Testing Best Practices

1. **Follow Protocol Exactly**: Don't skip steps, even if they seem optional
2. **Read Responses**: Verify each step worked before proceeding
3. **Handle Errors Gracefully**: Show what went wrong and where
4. **Clean Up Resources**: Always terminate subprocesses
5. **Test Real Scenarios**: Use actual queries that exercise your functionality

## Common MCP Protocol Mistakes

1. **Skipping Initialization**: Trying to use tools before `initialize`
2. **Missing Notifications**: Forgetting the `notifications/initialized` step
3. **Wrong Message Format**: Using request format for notifications
4. **Not Reading Responses**: Assuming requests worked without verification
5. **Protocol Version Mismatch**: Using unsupported protocol versions

---
*Understanding the protocol prevents mysterious errors and ensures reliable MCP servers.*
