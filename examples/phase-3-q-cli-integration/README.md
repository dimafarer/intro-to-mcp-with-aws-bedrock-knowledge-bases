# Phase 3: Q CLI Integration - Complete Example

This folder contains a complete, working implementation of Phase 3: Q CLI Integration with MCP server.

## What You'll Learn
- Configure MCP servers for Q CLI integration
- Handle virtual environment dependencies correctly
- Test end-to-end integration with Q CLI
- Troubleshoot common integration issues

## Prerequisites
- Completed Phase 2 (AWS Bedrock integration working)
- Q CLI installed and configured
- Understanding of virtual environments

## Files Included
- `src/mcp_bedrock_kb/server.py` - Complete MCP server with AWS integration
- `tests/test_q_cli_integration.py` - Q CLI integration validation
- `tests/test_mcp_protocol.py` - MCP protocol compliance test
- `requirements.txt` - Dependencies
- `lessons/` - Step-by-step tutorials (01, 02, 03, 04)
- `explanations/` - Detailed concept explanations

## Quick Start
**Prerequisites**: Ensure your AWS credentials and region are configured in `~/.aws/credentials` and `~/.aws/config`

```bash
# Navigate to the main project directory (NOT the examples folder)
cd /path/to/intro-to-mcp-with-aws-bedrock-knowledge-bases

# Edit configuration with your Knowledge Base ID and Model ARN
nano src/mcp_bedrock_kb/server.py
# Update line 19: KNOWLEDGE_BASE_ID = "YOUR_KNOWLEDGE_BASE_ID_HERE"
# Update line 74: 'modelArn': 'arn:aws:bedrock:YOUR_REGION::foundation-model/YOUR_MODEL_ID'

# Verify virtual environment exists (should already be created)
ls -la venv/bin/python
# Should show: venv/bin/python -> python3

# Install dependencies if needed
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Configure MCP server for Q CLI (using correct main project paths)
q mcp add --name bedrock-kb \
  --command /path/to/intro-to-mcp-with-aws-bedrock-knowledge-bases/venv/bin/python \
  --args "/path/to/intro-to-mcp-with-aws-bedrock-knowledge-bases/src/mcp_bedrock_kb/server.py" \
  --force

# Verify configuration
q mcp list
q mcp status --name bedrock-kb

# Test integration
cd /path/to/intro-to-mcp-with-aws-bedrock-knowledge-bases
python tests/test_q_cli_integration.py
```

## Learning Path
1. **Review Previous Phases**: Lessons 01-03 for foundation
2. **Q CLI Integration**: `lessons/04-q-cli-integration.md`
3. **Integration Concepts**: `explanations/q-cli-integration-explained.md`
4. **Test Setup**: Run integration tests
5. **Live Testing**: Use Q CLI with your enhanced knowledge base

## Testing Your Integration
```bash
# Start Q CLI chat
q chat

# Try these queries:
# "What tools do you have available?"
# "What is AWS Strands Agent framework?"
# "How do I create a Strands agent?"
```

## What's Working
✅ **Q CLI Registration**: MCP server properly configured
✅ **Virtual Environment**: Correct Python interpreter with dependencies
✅ **Tool Discovery**: Q CLI finds your `query_strands_docs` tool
✅ **End-to-End**: Real queries enhanced with Strands documentation
✅ **Error Handling**: Graceful AWS and integration error handling

## Troubleshooting
- **Server not starting**: Check virtual environment Python path
- **Tools not available**: Verify MCP protocol compliance
- **AWS errors**: Ensure credentials and permissions are correct
- **Timeout issues**: Consider increasing server timeout

## Next Phase
After mastering Q CLI integration, proceed to Phase 4: Q Developer Integration for IDE-based AI assistance.

---
*Your MCP server now enhances Q CLI with custom knowledge base queries!*
