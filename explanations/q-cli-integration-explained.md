# Q CLI Integration Explanation - Key Concepts

This document explains the important concepts behind integrating MCP servers with Q CLI, focusing on the "why" behind the configuration steps.

## Why Virtual Environment Paths Matter

### The Problem
When you run `python` in your terminal, it uses your activated virtual environment. But when Q CLI runs your MCP server, it starts a completely separate process that doesn't inherit your shell environment.

### What Happens Without Full Path
```bash
# This WILL FAIL when Q CLI tries to start your server
q mcp add --name bedrock-kb --command python --args "src/mcp_bedrock_kb/server.py"
```

**Why it fails**:
1. Q CLI starts a new process
2. Uses system Python (not your venv)
3. System Python doesn't have boto3, mcp libraries
4. Server crashes with "ModuleNotFoundError"

### The Solution
```bash
# This WORKS because it uses your venv Python with all dependencies
q mcp add --name bedrock-kb \
  --command /home/wsluser/projects/mcp-bedrock-kb/venv/bin/python \
  --args "src/mcp_bedrock_kb/server.py"
```

**Why it works**:
1. Full path points to venv Python interpreter
2. That Python has access to all installed packages
3. Server starts successfully with all dependencies

## How Q CLI Discovers and Launches MCP Servers

### Configuration Storage
Q CLI stores MCP server configurations in:
```
~/.aws/amazonq/mcp.json
```

### The Launch Process
1. **Discovery**: Q CLI reads mcp.json to find configured servers
2. **Launch**: Starts each server as a subprocess using the specified command
3. **Handshake**: Follows MCP protocol initialization sequence
4. **Tool Discovery**: Asks each server what tools it provides
5. **Integration**: Makes tools available during chat sessions

### What Q CLI Expects
Your MCP server must:
- Accept JSON-RPC messages on stdin
- Send responses on stdout
- Follow proper MCP initialization sequence
- Respond to `tools/list` and `tools/call` methods

## Common Integration Pitfalls

### 1. Wrong Python Interpreter
**Symptom**: Server fails to start, "ModuleNotFoundError"
**Cause**: Using system Python instead of venv Python
**Fix**: Use full path to venv Python interpreter

### 2. Working Directory Issues
**Symptom**: Server starts but can't find files
**Cause**: Q CLI runs server from different directory
**Fix**: Use absolute paths or ensure relative paths work from any directory

### 3. AWS Credentials Not Available
**Symptom**: Server starts but AWS calls fail
**Cause**: Server process doesn't inherit your AWS credentials
**Fix**: Ensure AWS credentials are in standard locations (~/.aws/)

### 4. Timeout Issues
**Symptom**: Server appears to work but tools aren't available
**Cause**: Server takes too long to start or respond
**Fix**: Increase timeout in MCP configuration

## Understanding the Integration Flow

### When You Ask Q CLI a Question
1. **Query Analysis**: Q CLI analyzes your question
2. **Tool Selection**: Decides if any MCP tools can help
3. **Tool Execution**: Calls your MCP server's tool
4. **Response Integration**: Combines tool output with AI response
5. **Final Answer**: Presents enhanced response to you

### Example Flow
```
You: "What is AWS Strands Agent framework?"
↓
Q CLI: Analyzes question, sees it might benefit from documentation
↓
Q CLI: Calls your query_strands_docs tool
↓
Your MCP Server: Queries Bedrock Knowledge Base
↓
Bedrock: Returns relevant Strands documentation
↓
Your MCP Server: Formats response with sources
↓
Q CLI: Integrates documentation into AI response
↓
You: Get enhanced answer with specific Strands information
```

## Debugging Integration Issues

### Check Server Registration
```bash
q mcp list
# Should show your server

q mcp status --name bedrock-kb
# Should show correct command and no errors
```

### Test Server Independently
```bash
# Test your server works outside Q CLI
cd /home/wsluser/projects/mcp-bedrock-kb
source venv/bin/activate
python tests/test_mcp_protocol.py
```

### Check Q CLI Logs
Q CLI may provide error messages when servers fail to start. Look for:
- Module import errors
- AWS credential errors
- Timeout errors
- Protocol compliance errors

## Best Practices for MCP Server Integration

### 1. Always Use Full Paths
- Python interpreter: Full path to venv Python
- Script paths: Consider using absolute paths
- File references: Use paths that work from any directory

### 2. Handle Errors Gracefully
- AWS credential errors should return helpful messages
- Network timeouts should be handled
- Invalid inputs should be validated

### 3. Optimize for Performance
- Cache responses when appropriate
- Set reasonable timeouts
- Minimize startup time

### 4. Test Integration Thoroughly
- Test server independently first
- Verify Q CLI can discover tools
- Test actual queries end-to-end
- Check error scenarios

## Why This Integration Approach Works

### Separation of Concerns
- **Q CLI**: Handles user interaction and AI responses
- **MCP Server**: Provides specialized tools and data access
- **Clean Interface**: Standard protocol for communication

### Scalability
- Multiple MCP servers can be configured
- Each server can provide multiple tools
- Tools can be enabled/disabled independently

### Maintainability
- MCP servers are independent processes
- Can be developed and tested separately
- Easy to update without affecting Q CLI

---
*Understanding these concepts prevents common integration issues and enables reliable MCP server deployment.*
