# MCP Bedrock Knowledge Base Server - Installation Guide

## Quick Setup for Q CLI and Q Developer

### Prerequisites
- Python 3.8+
- AWS CLI configured with credentials
- Q CLI installed

### Installation Steps

1. **Navigate to project directory**
```bash
cd /home/daddyfristy/mcpservers/intro-to-mcp-with-aws-bedrock-knowledge-bases
```

2. **Verify virtual environment exists** (should already be created)
```bash
ls -la venv/bin/python
# Should show: venv/bin/python -> python3
```

3. **Install dependencies** (if not already installed)
```bash
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

4. **Configure your AWS Knowledge Base ID** (edit the server.py file)
```bash
nano src/mcp_bedrock_kb/server.py
# Update line ~19: KNOWLEDGE_BASE_ID = "YOUR_KNOWLEDGE_BASE_ID_HERE"
# Update line ~74: 'modelArn': 'arn:aws:bedrock:YOUR_REGION::foundation-model/YOUR_MODEL_ID'
```

5. **Add MCP server to Q CLI**
```bash
q mcp add --name bedrock-kb \
  --command /home/daddyfristy/mcpservers/intro-to-mcp-with-aws-bedrock-knowledge-bases/venv/bin/python \
  --args "/home/daddyfristy/mcpservers/intro-to-mcp-with-aws-bedrock-knowledge-bases/src/mcp_bedrock_kb/server.py" \
  --force
```

6. **Verify installation**
```bash
q mcp list
q mcp status --name bedrock-kb
```

### Testing Your Setup

Start Q CLI and test the integration:
```bash
q chat
```

Try these queries in Q CLI:
- "What tools do you have available?"
- "What is AWS Strands Agent framework?"
- "How do I create a Strands agent?"

### For Q Developer (VS Code)

The same MCP server can be used with Q Developer. Add this configuration to your VS Code settings or Q Developer MCP configuration:

```json
{
  "mcpServers": {
    "bedrock-kb": {
      "command": "/home/daddyfristy/mcpservers/intro-to-mcp-with-aws-bedrock-knowledge-bases/venv/bin/python",
      "args": ["/home/daddyfristy/mcpservers/intro-to-mcp-with-aws-bedrock-knowledge-bases/src/mcp_bedrock_kb/server.py"]
    }
  }
}
```

### Troubleshooting

- **Server not starting**: Check that the virtual environment Python path exists
- **Tools not available**: Verify AWS credentials and Knowledge Base ID configuration
- **Permission errors**: Ensure the Python executable and server.py file are readable

### File Structure
```
/home/daddyfristy/mcpservers/intro-to-mcp-with-aws-bedrock-knowledge-bases/
├── venv/                          # Virtual environment (already created)
├── src/mcp_bedrock_kb/server.py   # Main MCP server file
├── requirements.txt               # Dependencies
└── INSTALLATION.md               # This file
```
