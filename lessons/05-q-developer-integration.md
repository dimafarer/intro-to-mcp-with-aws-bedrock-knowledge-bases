# Lesson 5: Q Developer Integration - IDE-Enhanced Development

## Learning Objectives
- Configure MCP server for Q Developer (IDE integration)
- Set up VS Code with Q Developer and MCP servers
- Enhance development workflow with custom knowledge base
- Test IDE-based AI assistance with Strands documentation

## What We're Building
Integrate our AWS Bedrock Knowledge Base MCP server with Q Developer in VS Code, enabling context-aware AI assistance during development with access to Strands Agent documentation.

## Prerequisites
- Completed Phase 3 (Q CLI integration working)
- VS Code installed
- Q Developer extension for VS Code
- Understanding of IDE development workflows

## Key Concepts

### Q Developer vs Q CLI
- **Q CLI**: Terminal-based AI assistance
- **Q Developer**: IDE-integrated AI assistance with code context
- **MCP Integration**: Both can use the same MCP servers

### IDE Integration Benefits
- **Code Context**: AI understands your current code
- **Inline Assistance**: Get help without leaving your editor
- **Project Awareness**: AI knows your project structure
- **Enhanced Responses**: Combine code context with custom knowledge

### Development Workflow Enhancement
1. **Code Analysis**: Q Developer analyzes your code
2. **Knowledge Augmentation**: MCP server provides domain-specific information
3. **Contextual Responses**: Combined insights for better assistance
4. **Iterative Development**: Continuous AI support during coding

## Implementation Steps

### Step 1: Verify Q Developer Extension

```bash
# Check if Q Developer extension is installed
code --list-extensions | grep amazon-q-vscode
# Should show: amazonwebservices.amazon-q-vscode
```

If not installed, install from VS Code marketplace:
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Amazon Q"
4. Install "Amazon Q" by Amazon Web Services

### Step 2: Verify MCP Configuration Sharing

Q Developer uses the same MCP configuration as Q CLI:

```bash
# Check your existing MCP configuration
cat ~/.aws/amazonq/mcp.json

# Should show your bedrock-kb server configuration
```

**Key Insight**: No additional configuration needed! Q Developer automatically discovers MCP servers configured for Q CLI.

### Step 3: Test Q Developer Integration

1. **Open VS Code in your project**:
   ```bash
   cd /home/wsluser/projects/mcp-bedrock-kb
   code .
   ```

2. **Open Q Developer Chat**:
   - Press `Ctrl+Shift+P` (Command Palette)
   - Type "Amazon Q: Open Chat"
   - Or click the Q icon in the sidebar

3. **Test Tool Discovery**:
   - In Q Developer chat, ask: "What tools do you have available?"
   - Should show your `query_strands_docs` tool

4. **Test Knowledge Base Integration**:
   - Ask: "What is AWS Strands Agent framework?"
   - Should get enhanced response from your knowledge base

### Step 4: Development Workflow Integration

**Context-Aware Assistance**:
1. Open a Python file in your project
2. Ask Q Developer: "How would I create a Strands agent for this project?"
3. Q Developer combines:
   - Your current code context
   - Strands documentation from your knowledge base
   - General AI knowledge

**Code-Specific Queries**:
1. Select some code in your editor
2. Ask: "How does this relate to Strands agent patterns?"
3. Get contextual responses using your custom knowledge

## Understanding IDE Integration

📖 **[Q Developer Integration Explained](../explanations/q-developer-integration-explained.md)** - How IDE context enhances MCP server responses

### Key Concepts
- **Shared Configuration**: Q Developer uses same MCP config as Q CLI
- **Context Enhancement**: Combines code context with knowledge base responses
- **Development Workflow**: Integrated assistance during coding
- **Performance Optimization**: Efficient resource usage in IDE environment

### Shared MCP Configuration
```json
{
  "mcpServers": {
    "bedrock-kb": {
      "command": "/path/to/your/venv/bin/python",
      "args": ["src/mcp_bedrock_kb/server.py"],
      "env": {},
      "timeout": 120000,
      "disabled": false
    }
  }
}
```

### VS Code Settings (Optional)
You can customize Q Developer behavior in VS Code settings:
```json
{
  "amazonQ.enableCodeSuggestions": true,
  "amazonQ.enableChatCodeContext": true
}
```

## Testing Results

✅ **Extension Available**: Q Developer installed and active
✅ **MCP Discovery**: Automatically finds Q CLI MCP servers
✅ **Tool Integration**: `query_strands_docs` available in IDE
✅ **Context Awareness**: Combines code context with knowledge base
✅ **Development Workflow**: Enhanced assistance during coding

## IDE-Specific Benefits

### Code Context Integration
- **File Awareness**: Q Developer knows your current file
- **Project Structure**: Understands your project layout
- **Selected Code**: Can analyze highlighted code snippets
- **Enhanced Responses**: Combines context with knowledge base

### Development Workflow Enhancement
- **Inline Help**: Get assistance without leaving your editor
- **Code Generation**: Generate Strands-specific code patterns
- **Documentation**: Access Strands docs while coding
- **Best Practices**: Get guidance specific to your project

## Advanced Usage Patterns

### 1. Architecture Guidance
```
You: "I'm building a multi-agent system. What Strands patterns should I use?"
Q Developer: [Combines your code context + Strands documentation]
```

### 2. Code Review Assistance
```
You: [Select code] "Does this follow Strands best practices?"
Q Developer: [Analyzes code + references Strands guidelines]
```

### 3. Deployment Planning
```
You: "How should I deploy this Strands agent to AWS?"
Q Developer: [Project-specific deployment guidance from knowledge base]
```

## Troubleshooting IDE Integration

### Q Developer Not Finding Tools
- **Check MCP Config**: Ensure `~/.aws/amazonq/mcp.json` exists
- **Restart VS Code**: Sometimes needed after MCP changes
- **Check Extension**: Ensure Q Developer extension is active

### Tools Available But Not Working
- **Virtual Environment**: Verify Python path in MCP config
- **AWS Credentials**: Ensure available in IDE environment
- **Server Logs**: Check for startup errors

### Performance Issues
- **Timeout Settings**: Increase if AWS queries are slow
- **Cache Responses**: Consider caching for frequently asked questions
- **Resource Usage**: Monitor server resource consumption

## Best Practices for IDE Integration

### 1. Context-Aware Queries
- Reference specific files or code sections
- Ask about patterns relevant to your current work
- Use project-specific terminology

### 2. Iterative Development
- Ask follow-up questions based on responses
- Refine queries as you develop
- Build on previous conversations

### 3. Knowledge Base Optimization
- Keep Strands documentation current
- Add project-specific patterns to knowledge base
- Include deployment and configuration examples

## Next Steps
With Q Developer integration complete, you now have:
- Terminal AI assistance (Q CLI)
- IDE-integrated AI assistance (Q Developer)
- Both enhanced with your custom Strands knowledge base

Consider exploring:
- Multiple knowledge bases for different domains
- Custom tools for project-specific operations
- Advanced MCP server features

---
*Your development environment now has AI assistance enhanced with domain-specific knowledge!*
