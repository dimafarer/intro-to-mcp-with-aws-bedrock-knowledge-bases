# Security Policy

## Overview

This repository contains educational materials for building MCP (Model Context Protocol) servers that integrate with AWS Bedrock Knowledge Base. This document outlines security considerations, identified issues, and recommendations for safe usage.

## 🔒 Security Status

**Overall Assessment**: ✅ **SAFE FOR PUBLIC RELEASE**

This repository contains educational code and documentation with no embedded secrets or credentials. However, users must follow security best practices when implementing these patterns.

## 🚨 Security Considerations

### 1. Hardcoded Resource Identifiers

**Issue**: The repository contains hardcoded AWS resource identifiers for educational purposes.

**Locations**:
- Knowledge Base ID: `QVBQZMYI7R` (appears in multiple files)
- AWS Region: `us-west-2` (hardcoded in examples)
- Model ARN: `arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0`

**Risk Level**: 🟡 **LOW** - These are resource identifiers, not credentials

**Mitigation**:
- These IDs are safe to expose (they're resource names, not secrets)
- Users should replace with their own resource IDs
- Consider using environment variables in production

### 2. Local Development Paths

**Issue**: Documentation contains local file system paths.

**Locations**:
- `/home/wsluser/projects/mcp-bedrock-kb/` (appears in lessons and examples)
- Virtual environment paths with username

**Risk Level**: 🟢 **MINIMAL** - Educational context only

**Mitigation**:
- Paths are for educational demonstration
- Users will naturally replace with their own paths
- No sensitive information exposed

### 3. AWS Credentials Handling

**Issue**: Code requires AWS credentials but doesn't specify secure handling.

**Current Implementation**:
- Uses boto3 default credential chain
- Provides error messages for missing credentials
- No hardcoded credentials (✅ GOOD)

**Risk Level**: 🟡 **LOW** - Proper credential handling implemented

**Recommendations**:
- Always use IAM roles in production
- Never commit AWS credentials to version control
- Use least-privilege access policies
- Rotate credentials regularly

## 🛡️ Security Best Practices for Users

### AWS Security

#### Credential Management
```bash
# ✅ GOOD: Use AWS CLI configuration
aws configure

# ✅ GOOD: Use environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret

# ❌ BAD: Never hardcode in source code
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"  # DON'T DO THIS
```

#### IAM Permissions
Create a minimal IAM policy for MCP server usage:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": [
                "arn:aws:bedrock:*:*:knowledge-base/YOUR_KB_ID"
            ]
        }
    ]
}
```

#### Network Security
- Use VPC endpoints for Bedrock access when possible
- Implement proper network segmentation
- Consider using AWS PrivateLink for enhanced security

### Development Security

#### Environment Variables
```python
# ✅ GOOD: Use environment variables
import os
KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID')
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

# ❌ BAD: Hardcoded values in production
KNOWLEDGE_BASE_ID = "QVBQZMYI7R"  # Only for examples
```

#### Input Validation
```python
# ✅ GOOD: Validate user inputs
def validate_query(query: str) -> str:
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")
    if len(query) > 1000:
        raise ValueError("Query too long")
    return query.strip()

# Apply validation before AWS calls
validated_query = validate_query(user_input)
```

#### Error Handling
```python
# ✅ GOOD: Don't expose internal details
except ClientError as e:
    if e.response['Error']['Code'] == 'AccessDeniedException':
        return "Access denied. Check your permissions."
    else:
        return "An error occurred. Please try again."

# ❌ BAD: Exposing internal error details
except Exception as e:
    return f"Error: {str(e)}"  # May expose sensitive info
```

### Production Deployment

#### Container Security
```dockerfile
# ✅ GOOD: Use non-root user
FROM python:3.11-slim
RUN useradd -m -u 1000 appuser
USER appuser

# ✅ GOOD: Minimal dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

#### Monitoring and Logging
- Enable AWS CloudTrail for API call auditing
- Monitor for unusual access patterns
- Implement proper logging without exposing sensitive data
- Set up alerts for failed authentication attempts

## 🔍 Vulnerability Reporting

### Scope
We welcome security reports for:
- Code vulnerabilities in examples
- Documentation security issues
- Dependency vulnerabilities
- Configuration security problems

### How to Report
1. **Email**: Create an issue in the GitHub repository for non-sensitive issues
2. **Sensitive Issues**: For security vulnerabilities, please email the maintainers directly
3. **Include**: 
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### Response Timeline
- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Fix Timeline**: Depends on severity
  - Critical: Within 24 hours
  - High: Within 1 week
  - Medium: Within 1 month
  - Low: Next release cycle

## 📋 Security Checklist for Users

### Before Using This Code

- [ ] Replace hardcoded resource IDs with your own
- [ ] Set up proper AWS IAM permissions
- [ ] Configure AWS credentials securely
- [ ] Review and understand the code before running
- [ ] Test in a development environment first

### Before Production Deployment

- [ ] Use environment variables for all configuration
- [ ] Implement proper input validation
- [ ] Set up monitoring and logging
- [ ] Use least-privilege IAM policies
- [ ] Enable AWS CloudTrail
- [ ] Implement rate limiting
- [ ] Use HTTPS for all communications
- [ ] Regular security updates for dependencies

### Ongoing Security

- [ ] Regular dependency updates
- [ ] Monitor AWS CloudTrail logs
- [ ] Rotate AWS credentials regularly
- [ ] Review IAM permissions periodically
- [ ] Keep MCP and boto3 libraries updated
- [ ] Monitor for security advisories

## 📚 Security Resources

### AWS Security
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [AWS Bedrock Security](https://docs.aws.amazon.com/bedrock/latest/userguide/security.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### Python Security
- [Python Security Guidelines](https://python.org/dev/security/)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Bandit Security Linter](https://bandit.readthedocs.io/)

### MCP Security
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Security Considerations](https://modelcontextprotocol.io/docs/concepts/security)

## 🔄 Security Updates

This security policy will be updated as:
- New security features are added
- Vulnerabilities are discovered and fixed
- Best practices evolve
- Community feedback is received

**Last Updated**: 2025-08-30
**Version**: 1.0.0

---

## 📞 Contact

For security-related questions or concerns:
- Create a GitHub issue for general security questions
- Email maintainers directly for sensitive security issues
- Follow responsible disclosure practices

**Remember**: This is educational code. Always implement additional security measures for production use.
