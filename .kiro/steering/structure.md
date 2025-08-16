# Project Structure

## File Organization

```
aws-devops-strands-agent/
├── main.py              # Main entry point - full-featured agent
├── fast.py              # Fast entry point - knowledge-only agent
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Git ignore file
├── src/                # Source code package
│   ├── __init__.py
│   ├── core/           # Core application components
│   │   ├── __init__.py
│   │   ├── agent.py           # Main application orchestration
│   │   ├── fast_agent.py      # Ultra-fast knowledge-only agent
│   │   ├── mcp_manager.py     # MCP client lifecycle management
│   │   ├── exceptions.py      # Custom exception hierarchy
│   │   └── logger.py          # Centralized logging configuration
│   ├── tools/          # Agent tools and integrations
│   │   ├── __init__.py
│   │   └── websearch_tool.py  # Web search tool with DuckDuckGo
│   ├── utils/          # Utility functions and helpers
│   │   ├── __init__.py
│   │   ├── mcp_utils.py       # MCP server utilities
│   │   └── timeout_utils.py   # Timeout handling utilities
│   └── interfaces/     # User interfaces and interaction components
│       ├── __init__.py
│       └── cli_interface.py   # Interactive CLI interface
├── config/             # Configuration files
│   └── config.py       # Configuration constants and settings
├── docs/               # Documentation and guides
│   ├── IMPROVEMENTS.md        # Code quality improvements
│   ├── model_temperature.md   # Temperature configuration guide
│   ├── notes.txt             # Development notes
│   └── technical_blog_build_process.md
├── tests/              # Test scripts and utilities
│   ├── README.md              # Testing documentation
│   ├── test_mcp_usage.py      # MCP server connectivity tests
│   └── simple_mcp_test.py     # Basic functionality tests
└── .kiro/              # Kiro IDE configuration
    └── steering/       # AI assistant steering rules
        ├── structure.md       # Project structure guidelines
        ├── tech.md           # Technology stack information
        └── product.md        # Product overview
```

## Key Files

### Entry Points
- **main.py**: Main entry point for full-featured agent with all 21 tools
- **fast.py**: Fast entry point for ultra-fast knowledge-only agent

### Core Application (src/core/)
- **agent.py**: Main orchestration with improved architecture:
  - Application entry point with signal handling
  - Agent creation and configuration with 21 tools
  - Resource management with proper cleanup
  - Graceful shutdown handling
- **fast_agent.py**: Ultra-fast knowledge-only agent:
  - Instant responses (< 1 second) for common AWS questions
  - Clean response formatting with proper AgentResult handling
  - Enhanced error handling and input validation
  - Optimized for speed with 150-word response limit
- **mcp_manager.py**: MCP client lifecycle management:
  - Centralized MCP client setup and teardown
  - Tool loading with error handling
  - Context management for MCP connections
- **exceptions.py**: Custom exception hierarchy for better error handling
- **logger.py**: Centralized logging configuration with multiple loggers

### Tools & Utilities (src/tools/, src/utils/)
- **websearch_tool.py**: Web search tool with DuckDuckGo integration
- **mcp_utils.py**: MCP server utilities and configurations
- **timeout_utils.py**: Timeout handling utilities

### Interfaces (src/interfaces/)
- **cli_interface.py**: Interactive CLI interface with enhanced error handling

### Configuration & Documentation
- **config/config.py**: Configuration constants with validation
- **requirements.txt**: Dependencies (strands-agents, strands-agents-tools, ddgs, mcp)
- **docs/model_temperature.md**: Detailed temperature tuning guide
- **docs/IMPROVEMENTS.md**: Comprehensive code quality improvements documentation
- **docs/notes.txt**: Development commands and snippets

### Documentation
- **README.md**: Comprehensive project documentation with usage examples

## Code Conventions

### Python Style
- Use descriptive function names and docstrings
- Follow tool decorator pattern for agent tools
- Environment variables for AWS configuration
- Exception handling for external API calls (DuckDuckGo)

### Agent Configuration
- System prompts optimized for AWS DevOps domain with efficiency guidelines and customer service standards
- Temperature setting of 0.3 for technical accuracy with validation
- Tools list combines websearch and triple MCP server tools (21 total tools)
- MCP tools managed by MCPManager with proper lifecycle handling
- Tool information stored for enhanced discovery and categorization
- Knowledge-first approach with minimal tool calls (max 1 per response)
- Enhanced error handling with custom exception types
- Customer-focused behavioral rules for friendly, helpful interactions

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