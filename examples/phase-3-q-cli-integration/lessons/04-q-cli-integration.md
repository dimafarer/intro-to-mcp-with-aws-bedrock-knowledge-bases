# Lesson 4: Q CLI Integration - Making Your MCP Server Available

## Learning Objectives
- Configure MCP server for Q CLI integration
- Test real-world usage with Q CLI
- Understand MCP server deployment
- Validate end-to-end functionality

## What We're Building
Connect our AWS Bedrock Knowledge Base MCP server to Q CLI so you can ask questions about Strands Agent documentation directly in your terminal.

## Prerequisites
- Completed Phase 2 (AWS Bedrock integration working)
- Q CLI installed and configured
- AWS credentials with Bedrock access

## Key Concepts

### MCP Server Configuration
Q CLI discovers MCP servers through configuration files that specify:
- **Server executable**: Path to your MCP server
- **Server arguments**: How to run it
- **Server name**: Identifier for the server

### Integration Flow
1. **Configure**: Tell Q CLI about your MCP server
2. **Start**: Q CLI launches your server automatically
3. **Query**: Ask questions that use your knowledge base
4. **Response**: Get enhanced answers from Strands documentation

## Implementation Steps

### Step 1: Configure MCP Server with Virtual Environment

**Critical**: Q CLI must use your project's virtual environment Python!

```bash
# Navigate to your project directory
cd /home/wsluser/projects/mcp-bedrock-kb

# Get the full path to your virtual environment Python
source venv/bin/activate
which python
# Output: /home/wsluser/projects/mcp-bedrock-kb/venv/bin/python

# Add MCP server using the FULL PATH to virtual environment Python
q mcp add --name bedrock-kb \
  --command /home/wsluser/projects/mcp-bedrock-kb/venv/bin/python \
  --args "src/mcp_bedrock_kb/server.py" \
  --force
```

**Why full path matters**:
- Q CLI runs servers independently of your shell environment
- Ensures boto3, mcp, and other dependencies are available
- Prevents "ModuleNotFoundError" when Q CLI starts your server

**What this does**:
- Registers your MCP server with Q CLI
- Tells Q CLI how to launch your server (python + script path)
- Creates configuration in `~/.aws/amazonq/mcp.json`

### Step 2: Verify Server Registration

```bash
# List all configured MCP servers
q mcp list

# Check specific server status
q mcp status --name bedrock-kb
```

**Expected output**:
- Server appears in the list
- Status shows command, timeout, and configuration

### Step 3: Test Integration with Q CLI

```bash
# Start Q CLI chat session
q chat
```

**In the chat session, try**:
- "What tools do you have available?"
- "Can you query the Strands documentation for me?"
- "What is AWS Strands Agent framework?"

### Step 4: Validate Tool Usage

When Q CLI recognizes your tool, it will:
1. **Discover**: Find your `query_strands_docs` tool
2. **Execute**: Call it with user queries
3. **Display**: Show enhanced responses from your knowledge base

## Understanding the Integration

📖 **[Q CLI Integration Explained](../explanations/q-cli-integration-explained.md)** - Why virtual environment paths matter and how Q CLI launches MCP servers

### Key Concepts
- **Process Isolation**: Q CLI runs your server independently
- **Dependency Management**: Virtual environment ensures all packages available
- **Configuration Storage**: Settings stored in `~/.aws/amazonq/mcp.json`
- **Tool Discovery**: Q CLI finds and integrates your tools automatically

### MCP Server Configuration
```json
{
  "bedrock-kb": {
    "command": "python",
    "args": ["src/mcp_bedrock_kb/server.py"],
    "timeout": 120000,
    "disabled": false
  }
}
```

### Working Directory
Q CLI runs your server from the directory where you added it, so relative paths work correctly.

## Testing Results

✅ **Server Registration**: Successfully added to Q CLI configuration
✅ **Status Check**: Server shows as enabled and properly configured
✅ **Tool Discovery**: Q CLI can find and use your `query_strands_docs` tool
✅ **Real Queries**: Enhanced responses from Strands documentation

## Troubleshooting Common Issues

### Server Not Starting
- **Check paths**: Ensure `src/mcp_bedrock_kb/server.py` exists
- **Check permissions**: Make sure script is executable
- **Check dependencies**: Ensure virtual environment is activated

### Tool Not Available
- **Protocol compliance**: Verify MCP initialization sequence
- **Error handling**: Check server logs for AWS credential issues
- **Timeout**: Increase timeout if AWS queries are slow

### AWS Integration Issues
- **Credentials**: Ensure AWS CLI is configured
- **Permissions**: Verify Bedrock access permissions
- **Region**: Check Knowledge Base region matches server configuration

## Advanced Configuration

### Environment Variables
```bash
q mcp add --name bedrock-kb \
  --command python \
  --args "src/mcp_bedrock_kb/server.py" \
  --env "AWS_REGION=us-west-2" \
  --env "KNOWLEDGE_BASE_ID=QVBQZMYI7R"
```

### Custom Timeout
```bash
q mcp add --name bedrock-kb \
  --command python \
  --args "src/mcp_bedrock_kb/server.py" \
  --timeout 180000  # 3 minutes for slow AWS queries
```

## Next Steps
Lesson 5 will cover:
- Advanced query features
- Performance optimization
- Multiple knowledge bases
- Production deployment considerations

---
*Your MCP server is now enhancing Q CLI with custom knowledge!*
