# Project Structure

## File Organization

```
aws-devops-strands-agent/
├── agent.py              # Main agent application with triple MCP integration
├── requirements.txt      # Python dependencies
├── model_temperature.md  # Temperature configuration guide
├── notes.txt            # Development notes
├── .gitignore           # Git ignore file for Python/AWS projects
├── README.md            # Project documentation
└── .kiro/               # Kiro IDE configuration
    └── steering/        # AI assistant steering rules
        ├── structure.md  # Project structure guidelines
        ├── tech.md       # Technology stack information
        └── product.md    # Product overview
```

## Key Files

### Core Application
- **agent.py**: Main entry point containing:
  - Agent initialization with BedrockModel
  - System prompt for AWS DevOps specialization with efficiency guidelines
  - Enhanced web search tool with timeout protection
  - Triple MCP client integration (AWS Documentation, Knowledge, EKS)
  - Dynamic tool loading with proper context management
  - Tool information storage and categorization
  - Interactive CLI loop with built-in tool discovery
  - Timeout protection for agent responses

### Configuration
- **requirements.txt**: Dependencies (strands-agents, strands-agents-tools, ddgs, mcp)
- **model_temperature.md**: Detailed temperature tuning guide
- **notes.txt**: Development commands and snippets

### Documentation
- **README.md**: Comprehensive project documentation with usage examples

## Code Conventions

### Python Style
- Use descriptive function names and docstrings
- Follow tool decorator pattern for agent tools
- Environment variables for AWS configuration
- Exception handling for external API calls (DuckDuckGo)

### Agent Configuration
- System prompts should be specific to AWS DevOps domain with CRITICAL EFFICIENCY GUIDELINES
- Temperature setting of 0.3 for technical accuracy
- Tools list combines websearch and triple MCP server tools (21 total tools)
- MCP tools are dynamically loaded with proper context management
- Tool information is stored for enhanced discovery and categorization
- Knowledge-first approach with minimal tool calls (max 1 per response)

### Error Handling
- Graceful handling of rate limits and API exceptions
- User-friendly error messages in CLI interface
- Fallback responses when external services fail
- Timeout protection for web searches (10 seconds)
- Timeout protection for agent responses (30 seconds)
- Proper MCP client lifecycle management with ExitStack
- Continues operation even if some MCP servers fail to load