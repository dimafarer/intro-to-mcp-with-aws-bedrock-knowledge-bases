# Lesson 3: AWS Bedrock Knowledge Base Integration

## Learning Objectives
- Connect MCP server to AWS Bedrock Knowledge Base
- Implement real query functionality
- Handle AWS authentication and responses
- Format knowledge base results for AI assistants

## Prerequisites
- Completed Phase 1 (MCP server foundation)
- AWS CLI configured with credentials
- AWS Bedrock Knowledge Base created (we have ID: QVBQZMYI7R)

## What We're Building
Transform our placeholder query function into a real AWS Bedrock Knowledge Base client that can:
1. Authenticate with AWS
2. Query the Strands Agent documentation
3. Format responses for AI assistants
4. Handle errors gracefully

## Key AWS Concepts

### Bedrock Knowledge Base
- **What**: Managed service for RAG (Retrieval Augmented Generation)
- **Why**: Provides semantic search over your documents
- **How**: We send queries, get relevant document chunks back

### Authentication
- **boto3**: Uses AWS credentials from CLI/environment
- **Region**: Must match where your Knowledge Base is deployed
- **Permissions**: Need bedrock:RetrieveAndGenerate permissions

## Implementation Steps

### Step 1: Update Server Configuration
```python
# Configuration
KNOWLEDGE_BASE_ID = "QVBQZMYI7R"
AWS_REGION = "us-west-2"
```

### Step 2: Implement Real Query Function
Replace the placeholder with actual AWS Bedrock client:
- Create `bedrock-agent-runtime` client
- Call `retrieve_and_generate` API
- Format response with query, answer, and sources

### Step 3: Add Comprehensive Error Handling
- AWS credentials missing
- Permission denied errors
- Service errors and rate limiting
- Unexpected errors

### Step 4: Test the Integration
```bash
# Test with proper MCP protocol
python tests/test_mcp_protocol.py
```

## Code Deep Dive

📖 **[AWS Integration Explained](../explanations/aws-integration-explained.md)** - Line-by-line breakdown of Bedrock integration

### Key Implementation Points

**Authentication**: Uses boto3 automatic credential discovery
**Query API**: `retrieve_and_generate` combines search + generation
**Response Format**: Structured output with Query, Answer, Sources
**Error Handling**: User-friendly messages for common issues

## Testing Results

✅ **MCP Protocol**: Server initializes and lists tools correctly
✅ **AWS Connection**: Successfully queries Bedrock Knowledge Base
✅ **Real Responses**: Gets actual answers from Strands documentation
✅ **Error Handling**: Gracefully handles missing credentials and permissions

## Sample Query Result
```
Query: What is AWS Strands?

Answer: AWS Strands is a Python SDK that provides tools and utilities 
for building and deploying AI agents and applications. It includes 
features for agent development, model integration, multi-agent systems, 
safety and security, observability and evaluation, and deployment 
options like AWS Lambda, AWS Fargate, and Amazon EC2.

Sources:
1. s3://your-bucket/strands-docs/overview.md
```

## Next Steps
Lesson 4 will cover:
- Integrating with Q CLI
- Advanced query features
- Performance optimization
- Production deployment

---
*From placeholder to production-ready AWS integration*
