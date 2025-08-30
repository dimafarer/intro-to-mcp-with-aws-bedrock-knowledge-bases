# Test Script Code Explanation - Line by Line

This document explains every line of our test script for new programmers. We'll cover subprocess communication, JSON-RPC, and testing concepts.

## File: `test_basic.py`

### The Shebang and Docstring

```python
#!/usr/bin/env python3
```
**What**: Shebang line (same as in server.py).
**Why**: Makes the file executable directly from command line.

```python
"""
Simple test script to understand MCP server communication

This script demonstrates:
1. How to start our MCP server
2. Basic tool discovery
3. Simple tool execution
"""
```
**What**: Module docstring explaining the test's purpose.
**Why**: Tests are documentation too! This tells future developers what we're testing and why.

### Imports - The Tools We Need

```python
import asyncio
```
**What**: Async programming library.
**Why**: Our test needs to coordinate timing and handle async operations.

```python
import json
```
**What**: Python's built-in JSON library.
**Why**: MCP uses JSON-RPC protocol. We need to create JSON messages and parse JSON responses.

```python
import subprocess
```
**What**: Library for running other programs from Python.
**Why**: We need to start our MCP server as a separate process and communicate with it.

```python
import sys
```
**What**: System-specific parameters and functions.
**Why**: We need `sys.executable` to find the Python interpreter path.

```python
from pathlib import Path
```
**What**: Modern way to handle file paths in Python.
**Why**: More reliable than string manipulation for file paths. Works on Windows, Mac, and Linux.

### The Main Test Function

```python
async def test_mcp_server():
```
**What**: Async function that contains our test logic.
**Why**: Async because we need to coordinate timing with the server process.

```python
"""Test our MCP server basic functionality"""
```
**What**: Function docstring.

```python
print("🧪 Testing MCP Server Basic Functionality")
print("=" * 50)
```
**What**: User-friendly output to show what's happening.
**Why**: Good tests provide clear feedback. The `"=" * 50` creates a line of 50 equal signs for visual separation.

### Finding Our Server

```python
server_path = Path(__file__).parent / "src" / "mcp_bedrock_kb" / "server.py"
```
**What**: Builds the path to our server file.
**Why**: We need to tell subprocess where to find our server.

**Breaking it down**:
- `Path(__file__)`: Path to the current test file
- `.parent`: Go up one directory (from test file to project root)
- `/ "src" / "mcp_bedrock_kb" / "server.py"`: Navigate to server file
- The `/` operator joins path parts (works on all operating systems)

### Starting the Server Process

```python
try:
```
**What**: Start of error handling block.
**Why**: Subprocess operations can fail. We want to handle errors gracefully.

```python
print("1. Starting MCP server...")
process = subprocess.Popen(
    [sys.executable, str(server_path)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
```
**What**: Starts our MCP server as a separate process.
**Why**: MCP servers run independently. We need to test them as they'll actually be used.

**Breaking down subprocess.Popen**:
- `[sys.executable, str(server_path)]`: Command to run (like typing `python server.py`)
- `sys.executable`: Path to Python interpreter (handles virtual environments correctly)
- `str(server_path)`: Convert Path object to string
- `stdin=subprocess.PIPE`: We can send input to the process
- `stdout=subprocess.PIPE`: We can read output from the process
- `stderr=subprocess.PIPE`: We can read error messages
- `text=True`: Handle input/output as text strings (not bytes)

### Test 1: Server Initialization

```python
print("2. Testing initialization...")
init_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
}
```
**What**: Creates a JSON-RPC initialization message.
**Why**: MCP protocol requires initialization before any other operations.

**Breaking down JSON-RPC structure**:
- `"jsonrpc": "2.0"`: Protocol version (standard requirement)
- `"id": 1`: Unique identifier for this request (so we can match responses)
- `"method": "initialize"`: What we want the server to do
- `"params"`: Parameters for the method
  - `"protocolVersion"`: Which MCP version we support
  - `"capabilities"`: What features we (the client) support
  - `"clientInfo"`: Information about our test client

```python
process.stdin.write(json.dumps(init_request) + "\n")
process.stdin.flush()
```
**What**: Sends the JSON message to our server.
**Why**: This is how we communicate with the server process.

**Breaking it down**:
- `json.dumps(init_request)`: Convert Python dictionary to JSON string
- `+ "\n"`: Add newline (JSON-RPC messages are line-separated)
- `process.stdin.write()`: Send to server's input
- `process.stdin.flush()`: Force immediate sending (don't buffer)

```python
response_line = process.stdout.readline()
if response_line:
    response = json.loads(response_line)
    print(f"   ✅ Server initialized: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
```
**What**: Reads and parses the server's response.
**Why**: We need to verify the server responded correctly.

**Breaking it down**:
- `process.stdout.readline()`: Read one line from server output
- `if response_line:`: Check if we got a response
- `json.loads(response_line)`: Convert JSON string back to Python dictionary
- `response.get('result', {})`: Safely get 'result' field, default to empty dict
- `.get('serverInfo', {}).get('name', 'Unknown')`: Chain of safe gets to extract server name

### Test 2: Tool Discovery

```python
print("3. Testing tool discovery...")
tools_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
}
```
**What**: Creates request to list available tools.
**Why**: Clients need to know what tools are available before using them.

**Key differences from init request**:
- `"id": 2`: Different ID (each request needs unique ID)
- `"method": "tools/list"`: Different method
- `"params": {}`: Empty parameters (this method doesn't need any)

```python
process.stdin.write(json.dumps(tools_request) + "\n")
process.stdin.flush()

response_line = process.stdout.readline()
if response_line:
    response = json.loads(response_line)
    tools = response.get('result', {}).get('tools', [])
    print(f"   ✅ Found {len(tools)} tools:")
    for tool in tools:
        print(f"      - {tool.get('name')}: {tool.get('description')}")
```
**What**: Same pattern - send request, read response, parse and display results.
**Why**: Consistent communication pattern makes code predictable.

**New concepts**:
- `tools = response.get('result', {}).get('tools', [])`: Extract tools list, default to empty list
- `len(tools)`: Count how many tools we found
- `for tool in tools:`: Loop through each tool to display details

### Test 3: Tool Execution

```python
print("4. Testing tool execution...")
call_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "query_strands_docs",
        "arguments": {"query": "What is AWS Strands?"}
    }
}
```
**What**: Creates request to execute a specific tool.
**Why**: This tests the actual functionality - can we call our tool and get a response?

**New parameter structure**:
- `"name": "query_strands_docs"`: Which tool to call
- `"arguments": {"query": "What is AWS Strands?"}`: Input data for the tool

```python
process.stdin.write(json.dumps(call_request) + "\n")
process.stdin.flush()

response_line = process.stdout.readline()
if response_line:
    response = json.loads(response_line)
    content = response.get('result', {}).get('content', [])
    if content:
        print(f"   ✅ Tool response: {content[0].get('text', 'No text')[:100]}...")
```
**What**: Same communication pattern, but extracts tool response content.
**Why**: Tool responses contain the actual data we're interested in.

**New concepts**:
- `content = response.get('result', {}).get('content', [])`: Extract content array
- `if content:`: Check if we got any content
- `content[0].get('text', 'No text')`: Get text from first content item
- `[:100]`: Truncate to first 100 characters for display
- `+ "..."`: Add ellipsis to show truncation

### Cleanup and Error Handling

```python
print("\n🎉 Basic MCP server test completed!")

except Exception as e:
    print(f"❌ Test failed: {e}")
finally:
    if 'process' in locals():
        process.terminate()
        process.wait()
```
**What**: Handles success, errors, and cleanup.
**Why**: Good tests always clean up after themselves.

**Breaking it down**:
- `except Exception as e:`: Catch any error that occurred
- `print(f"❌ Test failed: {e}")`: Show what went wrong
- `finally:`: Always runs, even if there was an error
- `if 'process' in locals():`: Check if we created a process
- `process.terminate()`: Ask the process to stop
- `process.wait()`: Wait for it to actually stop

### Script Entry Point

```python
if __name__ == "__main__":
    asyncio.run(test_mcp_server())
```
**What**: Runs our test when script is executed directly.
**Why**: Standard Python pattern for executable scripts.

## Key Testing Concepts for New Programmers

### 1. Subprocess Communication
- **Why**: Tests need to run programs as they'll actually be used
- **How**: `subprocess.Popen` creates separate processes
- **Communication**: stdin/stdout pipes let us send/receive data

### 2. JSON-RPC Protocol
- **Structure**: Every message has jsonrpc, id, method, params
- **IDs**: Match requests to responses
- **Methods**: Tell the server what to do

### 3. Error Handling in Tests
- **try/except**: Catch and report errors clearly
- **finally**: Always clean up resources
- **Graceful failure**: Tests should never leave processes running

### 4. Test Output
- **Clear messages**: Users should understand what's happening
- **Visual formatting**: Emojis and lines make output readable
- **Detailed results**: Show what worked and what didn't

## Why This Testing Approach?

1. **Real-world simulation**: Tests the server as it will actually be used
2. **Protocol validation**: Ensures we implement MCP correctly
3. **Clear feedback**: Easy to see what works and what doesn't
4. **Safe execution**: Proper cleanup prevents resource leaks
5. **Educational**: Shows how MCP communication actually works

## Common Issues New Programmers Face

1. **Forgetting newlines**: JSON-RPC messages must end with `\n`
2. **Not flushing**: Buffered output might not send immediately
3. **Process cleanup**: Always terminate subprocesses
4. **Error handling**: Network/process operations can fail
5. **Async timing**: Processes need time to start and respond
