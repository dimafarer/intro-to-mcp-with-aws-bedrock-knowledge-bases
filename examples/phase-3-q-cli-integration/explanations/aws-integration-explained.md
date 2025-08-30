# AWS Integration Code Explanation - Line by Line

This document explains the AWS Bedrock Knowledge Base integration for new programmers.

## New Imports and Configuration

```python
from botocore.exceptions import ClientError, NoCredentialsError
import json
```
**What**: Import AWS-specific error types and JSON handling.
**Why**: We need to handle AWS authentication errors and parse JSON responses gracefully.

```python
# Configuration
KNOWLEDGE_BASE_ID = "QVBQZMYI7R"
AWS_REGION = "us-west-2"
```
**What**: Constants for our specific AWS setup.
**Why**: Hardcoding these values makes the code clearer and easier to maintain. In production, these might come from environment variables.

## The Real Query Function

```python
async def query_knowledge_base(query: str) -> list[types.TextContent]:
    """Query the Bedrock Knowledge Base"""
    if not query.strip():
        return [types.TextContent(
            type="text",
            text="Please provide a query to search the Strands Agent documentation."
        )]
```
**What**: Input validation - check if query is empty or just whitespace.
**Why**: Better user experience than sending empty queries to AWS (which would cost money and return poor results).

### AWS Client Creation

```python
try:
    # Create Bedrock client
    bedrock_client = boto3.client(
        'bedrock-agent-runtime',
        region_name=AWS_REGION
    )
```
**What**: Creates an AWS client for Bedrock Agent Runtime service.
**Why**: This is how we communicate with AWS Bedrock. The `bedrock-agent-runtime` service handles knowledge base queries.

**Breaking it down**:
- `boto3.client()`: Creates AWS service client
- `'bedrock-agent-runtime'`: Specific AWS service for knowledge base operations
- `region_name=AWS_REGION`: Must match where your knowledge base is deployed

### Making the Query

```python
response = bedrock_client.retrieve_and_generate(
    input={
        'text': query
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': KNOWLEDGE_BASE_ID,
            'modelArn': 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'
        }
    }
)
```
**What**: Calls AWS Bedrock to query the knowledge base and generate an answer.
**Why**: This is the core RAG (Retrieval Augmented Generation) operation - it finds relevant documents and generates a coherent answer.

**Breaking down the parameters**:
- `input.text`: The user's question
- `type: 'KNOWLEDGE_BASE'`: We're querying a knowledge base (not just retrieving documents)
- `knowledgeBaseId`: Which knowledge base to search
- `modelArn`: Which AI model to use for generating the answer (Claude 3 Sonnet in this case)

### Response Processing

```python
# Extract the generated response
generated_text = response['output']['text']

# Format response with sources if available
formatted_response = f"**Query**: {query}\n\n**Answer**: {generated_text}"
```
**What**: Extracts the AI-generated answer and formats it nicely.
**Why**: Raw AWS responses are JSON objects. We want to present a clean, readable format to users.

### Adding Source Citations

```python
# Add source citations if available
if 'citations' in response and response['citations']:
    formatted_response += "\n\n**Sources**:"
    for i, citation in enumerate(response['citations'], 1):
        if 'retrievedReferences' in citation:
            for ref in citation['retrievedReferences']:
                if 'location' in ref and 's3Location' in ref['location']:
                    source_uri = ref['location']['s3Location'].get('uri', 'Unknown source')
                    formatted_response += f"\n{i}. {source_uri}"
```
**What**: Extracts and formats source document references.
**Why**: Users should know where information comes from. This builds trust and allows verification.

**Breaking down the nested structure**:
- `response['citations']`: List of source citations
- `enumerate(response['citations'], 1)`: Loop with numbering starting at 1
- `citation['retrievedReferences']`: Documents that were used
- `ref['location']['s3Location']['uri']`: Path to the source document

## Error Handling - Making It Robust

### AWS Credentials Error

```python
except NoCredentialsError:
    return [types.TextContent(
        type="text",
        text="❌ AWS credentials not found. Please configure AWS CLI with 'aws configure' or set environment variables."
    )]
```
**What**: Handles missing AWS credentials.
**Why**: Common issue for new users. Provides clear instructions on how to fix it.

### Permission Errors

```python
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'AccessDeniedException':
        return [types.TextContent(
            type="text",
            text="❌ Access denied. Please ensure your AWS credentials have bedrock:RetrieveAndGenerate permissions."
        )]
    else:
        return [types.TextContent(
            type="text",
            text=f"❌ AWS error ({error_code}): {e.response['Error']['Message']}"
        )]
```
**What**: Handles AWS permission and other service errors.
**Why**: AWS errors can be cryptic. We translate them into actionable messages.

**Breaking it down**:
- `ClientError`: AWS service errors (permissions, service limits, etc.)
- `e.response['Error']['Code']`: AWS error type
- `AccessDeniedException`: Specific permission error
- Generic error handling for other AWS issues

### Catch-All Error Handling

```python
except Exception as e:
    return [types.TextContent(
        type="text",
        text=f"❌ Unexpected error: {str(e)}"
    )]
```
**What**: Handles any other unexpected errors.
**Why**: Prevents the server from crashing and provides debugging information.

## Key AWS Concepts for New Programmers

### 1. AWS Authentication
- **boto3**: Automatically finds credentials from AWS CLI, environment variables, or IAM roles
- **Region**: AWS services are region-specific
- **Permissions**: Your credentials need specific permissions for each service

### 2. Bedrock Knowledge Base
- **RAG**: Retrieval Augmented Generation - finds relevant documents, then generates answers
- **Vector Search**: Uses AI embeddings to find semantically similar content
- **Foundation Models**: Large language models (like Claude) that generate human-like responses

### 3. Error Handling Patterns
- **Specific Errors First**: Handle known errors with helpful messages
- **Generic Errors Last**: Catch-all for unexpected issues
- **User-Friendly Messages**: Translate technical errors into actionable advice

### 4. Response Formatting
- **Structured Output**: Consistent format (Query, Answer, Sources)
- **Markdown**: Use `**bold**` for better readability
- **Source Attribution**: Always cite where information comes from

## Why This Structure?

1. **Robust Error Handling**: Gracefully handles common AWS issues
2. **Clear Response Format**: Consistent, readable output
3. **Source Attribution**: Builds trust and enables verification
4. **Input Validation**: Prevents unnecessary API calls
5. **Configuration**: Easy to modify for different knowledge bases

## Common Issues New Programmers Face

1. **AWS Credentials**: Forgetting to configure `aws configure`
2. **Permissions**: Not having the right IAM permissions
3. **Region Mismatch**: Knowledge base in different region than client
4. **Error Handling**: Not handling AWS service errors gracefully
5. **Response Parsing**: Not understanding nested JSON structure

## Production Considerations

- **Environment Variables**: Don't hardcode credentials or IDs
- **Rate Limiting**: Handle AWS throttling
- **Caching**: Cache responses to reduce costs
- **Logging**: Log queries for debugging and analytics
- **Cost Monitoring**: Track AWS usage and costs
