# Lesson 1: Building an MCP Server - Basics and Setup

## What is MCP (Model Context Protocol)?

MCP is an open protocol that standardizes how applications provide context to LLMs. It enables communication between AI assistants and locally running servers that provide additional tools and resources.

## Our Goal

Build an MCP server that connects to AWS Bedrock Knowledge Base to enhance AI assistants with domain-specific documentation (AWS Strands Agent docs).

## Prerequisites

- Python 3.8+
- AWS CLI configured with credentials
- AWS Bedrock Knowledge Base (we have this ready)

## Step 1: Project Structure

Let's create our project structure:

```
mcp-bedrock-kb/
├── src/
│   └── mcp_bedrock_kb/
│       ├── __init__.py
│       └── server.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Step 2: Development Environment Setup

### Git Repository
```bash
git init
# Create .gitignore for Python projects
```

### Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### Dependencies
```bash
pip install -r requirements.txt
```

Core dependencies:
- `mcp` - MCP protocol implementation  
- `boto3` - AWS SDK for Python

## Step 3: Testing Strategy

We'll implement testing at each milestone:
- Unit tests for individual functions
- Integration tests with mock AWS responses
- End-to-end tests with actual Bedrock KB

## Milestone 1 Commit

At this point we have:
- ✅ Project structure
- ✅ Git repository with .gitignore
- ✅ Virtual environment
- ✅ Basic MCP server skeleton
- ✅ Dependencies defined

**Question for you**: Should we add a `pyproject.toml` for modern Python packaging, or keep it simple with just `requirements.txt` for now?

## Next Steps

In lesson 2, we'll:
1. Install dependencies in our venv
2. Implement the Bedrock KB connection
3. Test with a simple query
4. Create our first git commit milestone

---
*This is a living document - we'll update as we build*
