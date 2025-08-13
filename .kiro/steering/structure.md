# Project Structure

## File Organization

```
aws-devops-strands-agent/
├── agent.py              # Main application orchestration (improved architecture)
├── mcp_manager.py        # MCP client lifecycle management
├── cli_interface.py      # Interactive CLI interface with enhanced error handling
├── config.py             # Configuration constants with validation
├── mcp_utils.py          # MCP server utilities and configurations
├── websearch_tool.py     # Web search tool with DuckDuckGo integration
├── exceptions.py         # Custom exception hierarchy for better error handling
├── logger.py            # Centralized logging configuration
├── requirements.txt      # Python dependencies
├── model_temperature.md  # Temperature configuration guide
├── IMPROVEMENTS.md       # Code quality improvements documentation
├── notes.txt            # Development notes
├── .gitignore           # Git ignore file for Python/AWS projects
├── README.md            # Project documentation
├── tests/               # Test scripts and utilities
│   ├── README.md        # Testing documentation
│   ├── test_mcp_usage.py # MCP server connectivity tests
│   └── simple_mcp_test.py # Basic functionality tests
└── .kiro/               # Kiro IDE configuration
    └── steering/        # AI assistant steering rules
        ├── structure.md  # Project structure guidelines
        ├── tech.md       # Technology stack information
        └── product.md    # Product overview
```

## Key Files

### Core Application
- **agent.py**: Main orchestration with improved architecture:
  - Application entry point with signal handling
  - Agent creation and configuration
  - Resource management with proper cleanup
  - Graceful shutdown handling
- **mcp_manager.py**: MCP client lifecycle management:
  - Centralized MCP client setup and teardown
  - Tool loading with error handling
  - Context management for MCP connections
- **exceptions.py**: Custom exception hierarchy for better error handling
- **logger.py**: Centralized logging configuration with multiple loggers

### Configuration & Documentation
- **config.py**: Configuration constants with validation
- **requirements.txt**: Dependencies (strands-agents, strands-agents-tools, ddgs, mcp)
- **model_temperature.md**: Detailed temperature tuning guide
- **IMPROVEMENTS.md**: Comprehensive code quality improvements documentation
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
- System prompts optimized for AWS DevOps domain with efficiency guidelines
- Temperature setting of 0.3 for technical accuracy with validation
- Tools list combines websearch and triple MCP server tools (21 total tools)
- MCP tools managed by MCPManager with proper lifecycle handling
- Tool information stored for enhanced discovery and categorization
- Knowledge-first approach with minimal tool calls (max 1 per response)
- Enhanced error handling with custom exception types

### Error Handling
- Custom exception hierarchy for specific error types
- Graceful handling of rate limits and API exceptions
- User-friendly error messages with context
- Fallback responses when external services fail
- Timeout protection for web searches (10 seconds)
- Timeout protection for agent responses (45 seconds)
- Proper MCP client lifecycle management with MCPManager
- Structured logging for debugging and monitoring
- Signal handlers for graceful shutdown
- Configuration validation at startup