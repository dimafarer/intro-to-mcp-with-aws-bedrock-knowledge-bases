# Phase 2: AWS Integration - Complete Example

This folder contains a complete, working implementation of Phase 2: AWS Bedrock Knowledge Base Integration.

## What You'll Learn
- Connect MCP server to AWS Bedrock Knowledge Base
- Handle AWS authentication and errors
- Format responses with sources
- Real-world RAG (Retrieval Augmented Generation)

## Prerequisites
- Completed Phase 1 (or understand MCP basics)
- AWS CLI configured with credentials
- AWS Bedrock Knowledge Base access

## Files Included
- `src/mcp_bedrock_kb/server.py` - Complete MCP server with AWS integration
- `tests/test_mcp_protocol.py` - Working MCP protocol test
- `tests/test_basic.py` - Phase 1 reference test
- `requirements.txt` - Dependencies
- `lessons/` - Step-by-step tutorials (01, 02, 03)
- `explanations/` - Line-by-line code explanations

## Quick Start
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Test the AWS integration
python tests/test_mcp_protocol.py
```

## Learning Path
1. **Review Phase 1**: `lessons/01-mcp-basics.md` and `lessons/02-testing-basics.md`
2. **AWS Integration**: `lessons/03-aws-integration.md`
3. **Code Deep Dive**: `explanations/aws-integration-explained.md`
4. **Test It**: `python tests/test_mcp_protocol.py`
5. **Experiment**: Try different queries!

## Sample Queries to Try
- "What is AWS Strands Agent framework?"
- "How do I create a Strands agent?"
- "What are the deployment options for Strands?"

## What's Working
✅ **Real AWS Queries**: Connects to Bedrock Knowledge Base (ID: QVBQZMYI7R)
✅ **Error Handling**: Graceful AWS credential and permission errors
✅ **Response Formatting**: Query + Answer + Sources
✅ **MCP Protocol**: Full compliance with proper initialization

## Next Phase
After mastering AWS integration, proceed to Phase 3: Q CLI Integration and Advanced Features.

---
*This is a complete, standalone example. You can modify it without affecting other phases.*
