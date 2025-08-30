# MCP Bedrock Knowledge Base Server - Learning Guide

Learn to build MCP (Model Context Protocol) servers that connect to AWS Bedrock Knowledge Base for enhanced AI assistance.

## 🎯 Learning Objectives
1. Understand MCP server fundamentals
2. Connect MCP servers to AWS Bedrock Knowledge Base
3. Integrate with AI assistants (Q CLI, Q Developer)
4. Create comprehensive documentation and testing

## 📚 Choose Your Learning Path

### Path A: Example Folders (Recommended for Beginners)
**Best for**: New programmers, those unfamiliar with git

```bash
# Clone the repository
git clone <repository-url>
cd mcp-bedrock-kb

# Start with Phase 1
cd examples/phase-1-foundation
# Follow the README in that folder
```

**Advantages**:
- No git knowledge required
- Complete working examples
- Can't accidentally break previous work
- Easy to compare phases side-by-side

### Path B: Git Tags (Recommended for Intermediate+)
**Best for**: Developers familiar with git, want to see progression

```bash
# Clone the repository
git clone <repository-url>
cd mcp-bedrock-kb

# Start with Phase 1
git checkout phase-1-complete
# Follow lessons/01-mcp-basics.md

# Later, move to Phase 2
git checkout phase-2-complete
```

**Advantages**:
- Learn professional git workflow
- See exact code changes between phases
- Understand development progression
- Practice version control

## 📖 Learning Phases

### Phase 1: Foundation ✅
**Status**: Complete
- Basic MCP server structure
- Tool registration and handling
- Testing methodology
- Comprehensive documentation

**Files**: `examples/phase-1-foundation/` or `git checkout phase-1-complete`

### Phase 2: AWS Integration ✅
**Status**: Complete
- Connect to Bedrock Knowledge Base
- Real query implementation
- Response formatting
- AWS authentication

**Files**: `examples/phase-2-aws-integration/` or `git checkout phase-2-complete`

### Phase 3: Advanced Features 📋
**Status**: Planned
- Error handling and resilience
- Performance optimization
- Multiple knowledge bases
- Production deployment

## 🛠️ Prerequisites
- Python 3.8+
- AWS CLI configured with credentials
- AWS Bedrock Knowledge Base (optional - we'll help you create one)

## 🚀 Quick Start (Either Path)
1. Choose your learning path above
2. Follow the README in your chosen starting point
3. Work through lessons sequentially
4. Experiment and modify the code!

## 📋 Project Structure
```
mcp-bedrock-kb/
├── examples/                      # Complete phase examples
│   ├── phase-1-foundation/       # Standalone working example
│   └── phase-2-aws-integration/  # AWS Bedrock KB integration
├── src/                          # Current development
├── lessons/                      # Step-by-step tutorials
│   ├── 01-mcp-basics.md
│   ├── 02-testing-basics.md
│   └── 03-aws-integration.md
├── explanations/                 # Detailed code explanations
│   ├── server-explained.md
│   ├── test-explained.md
│   └── aws-integration-explained.md
├── tests/                        # Test files
│   ├── test_basic.py            # Phase 1 reference
│   └── test_mcp_protocol.py     # Current working test
├── README.md                     # This file
└── implementation-plan.md        # Development roadmap
```

## 🎓 Educational Features
- **Line-by-line explanations**: Every line of code explained for new programmers
- **Why-focused learning**: Understanding the reasoning behind each decision
- **Real-world testing**: Learn to test MCP servers properly
- **Professional practices**: Git workflow, documentation, error handling

## 🤝 Contributing
This is an educational project. Feel free to:
- Suggest improvements to explanations
- Report unclear documentation
- Share your learning experience
- Propose additional examples

---
**Happy Learning!** 🎉

*Choose your path above and start building MCP servers that enhance AI assistants with your own knowledge bases.*
