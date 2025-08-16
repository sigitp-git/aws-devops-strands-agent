# Building an AWS DevOps AI Agent with Strands Framework: A Technical Deep Dive

## Introduction

Building intelligent AI agents for specialized domains requires careful architecture, robust error handling, and seamless integration of multiple data sources. This technical blog explores the complete build process of an AWS DevOps AI agent built with the Strands Agents framework, powered by Claude Sonnet 4 on AWS Bedrock, and enhanced with real-time web search and comprehensive AWS documentation access.

## Architecture Overview

The agent follows a modular, production-ready architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Interface │    │  Agent Core      │    │  Tool Ecosystem │
│                 │    │                  │    │                 │
│ • User Input    │◄──►│ • Claude Sonnet 4│◄──►│ • Web Search    │
│ • Tool Display  │    │ • Strands Agent  │    │ • AWS Docs MCP  │
│ • Error Handling│    │ • Context Mgmt   │    │ • AWS Knowledge │
└─────────────────┘    └──────────────────┘    │ • AWS EKS MCP   │
                                               └─────────────────┘
           ▲                       ▲                       ▲
           │                       │                       │
    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │Configuration│         │   Logging   │         │MCP Manager  │
    │& Validation │         │& Monitoring │         │& Lifecycle  │
    └─────────────┘         └─────────────┘         └─────────────┘
```

## Core Technology Stack

### Foundation Layer
- **Strands Agents Framework**: Primary agent orchestration with enhanced architecture
- **AWS Bedrock**: Claude Sonnet 4 model hosting (`us.anthropic.claude-sonnet-4-20250514-v1:0`)
- **Python 3.10+**: Runtime with full type hints and modern features

### Integration Layer
- **Model Context Protocol (MCP)**: Real-time AWS service integration
- **DuckDuckGo SDK**: Web search with timeout protection
- **uvx/uv**: Python package manager for MCP server execution

### AWS Services
- **AWS Bedrock**: Model hosting in us-east-1 region
- **AWS IAM**: Authentication and authorization
- **AWS EKS**: Direct cluster management capabilities

## Build Process Deep Dive

### Phase 1: Core Agent Setup

The foundation starts with creating a robust agent configuration:

```python
# agent.py - Main orchestration
def create_agent() -> tuple[Agent, int, list, list]:
    """Create and configure the agent with all available tools."""
    # Create Bedrock model with optimized temperature
    model = BedrockModel(model_id=MODEL_ID, temperature=0.3)
    
    # Initialize with web search baseline
    tools = [websearch]
    
    # Load MCP tools dynamically
    mcp_manager = MCPManager()
    mcp_tools, mcp_tool_info, mcp_clients = mcp_manager.load_mcp_tools()
    tools.extend(mcp_tools)
    
    # Create agent with efficiency-optimized prompt
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=tools)
    
    return agent, len(tools), mcp_tool_info, mcp_clients
```

### Phase 2: MCP Integration Architecture

The Model Context Protocol integration provides real-time AWS access:

```python
# mcp_manager.py - Centralized MCP lifecycle management
class MCPManager:
    """Manages MCP clients and tool loading with proper lifecycle management."""
    
    def load_mcp_tools(self) -> Tuple[List, List[Dict[str, Any]], List]:
        """Load tools from all configured MCP servers."""
        return self._load_servers(MCP_SERVERS)
    
    def _load_servers(self, server_configs: List[Dict]):
        """Load tools from specified server configurations."""
        for server_config in server_configs:
            try:
                client = create_mcp_client(
                    server_config["command"], 
                    server_config["args"],
                    server_config.get("env")
                )
                
                # Context-managed tool loading
                with client:
                    mcp_tools = client.list_tools_sync()
                    # Store tool metadata for discovery
                    self._extract_tool_info(mcp_tools, server_config['name'])
                    
                self.clients.append(client)
                
            except Exception as e:
                self._handle_server_error(server_config['name'], e)
```

### Phase 3: Multi-Source Tool Integration

The agent integrates three distinct MCP servers for comprehensive AWS coverage:

```python
# mcp_utils.py - Server configurations
MCP_SERVERS = [
    {
        "name": "AWS Documentation",
        "command": "uvx",
        "args": ["awslabs.aws-documentation-mcp-server@latest"]
    },
    {
        "name": "AWS Knowledge", 
        "command": "uvx",
        "args": [
            "mcp-proxy",
            "--transport", "streamablehttp",
            "https://knowledge-mcp.global.api.aws"
        ]
    },
    {
        "name": "AWS EKS",
        "command": "uvx",
        "args": [
            "awslabs.eks-mcp-server@latest",
            "--allow-write",
            "--allow-sensitive-data-access"
        ],
        "env": {
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_REGION": "us-east-1"
        }
    }
]
```

This provides:
- **21 total tools** when all servers are available
- **Graceful degradation** to web search if MCP servers fail
- **Real-time AWS documentation** access
- **Direct EKS cluster management** capabilities

### Phase 4: Enhanced Web Search Implementation

The web search tool includes sophisticated timeout protection and performance optimization:

```python
# websearch_tool.py - Optimized web search
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = 3) -> str:
    """Search the web with timeout protection and smart result limiting."""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Search timeout after {SEARCH_TIMEOUT_SECONDS} seconds")
    
    try:
        # 10-second timeout protection
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(SEARCH_TIMEOUT_SECONDS)
        
        # Smart result limiting for performance
        if max_results is None or max_results > MAX_SEARCH_RESULTS_LIMIT:
            max_results = DEFAULT_MAX_SEARCH_RESULTS
            
        print(f"🔍 Searching for: {keywords}")
        results = DDGS().text(keywords, region=region, max_results=max_results)
        
        if results:
            print(f"✅ Found {len(results)} results")
            return results
        else:
            return "No results found."
            
    except TimeoutError:
        return "Search timeout - please try a more specific query."
    except RatelimitException:
        return "Rate limit reached - please try again in a moment."
    finally:
        signal.alarm(0)  # Always cancel timeout
```

Key features:
- **10-second timeout protection** prevents hanging searches
- **Smart result limiting** (default 3, max 5) for faster responses
- **Visual feedback** with progress indicators
- **Comprehensive error handling** for rate limits and timeouts

### Phase 5: Configuration Management and Validation

Robust configuration with early validation prevents runtime errors:

```python
# config.py - Configuration with validation
@dataclass(frozen=True)
class ModelConfig:
    """Model configuration with validation."""
    MODEL_ID: ClassVar[str] = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
    MODEL_TEMPERATURE: ClassVar[float] = 0.3
    
    @classmethod
    def validate(cls) -> None:
        """Validate model configuration."""
        if not (0.0 <= cls.MODEL_TEMPERATURE <= 1.0):
            raise ConfigurationError(
                f"MODEL_TEMPERATURE must be between 0.0 and 1.0, got {cls.MODEL_TEMPERATURE}"
            )
figuration() -> None:
    """Validate all configuration values at startup."""
    ModelConfig.validate()
  
def validatonfig.validate()
```

Configuration features:catches errors at startup
- **Type safety** with dataclasses and ClassVar
- **Environment setup** for AWS regions
- **Immutable configuration** prevents accidental changes

### Phase 6: Error Handling and Resilience

Custom exception hierarchy provides better debugging and user experience:

```python
# exceptions.py - Custom exception hierarchy
class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass

class MCPConnectionError(AgentError):
    """Raised when MCP server connection fails."""
    def __init__(self, server_name: str, original_error: Exception):
        super().__init__(f"Failed to connect to {server_name}: {original_error}")

class AgentTimeoutError(AgentError):
    """Raised when agent response times     self.server_nameror = original_error
     = server_name"""
    def __init__(self, time
        self.origds: int):
        self.timeout_seconds = timeout_seconds
        super().__init__(f"Agent response timed out after {timeout_seconds} seconds")
```

Error handling benefits:
- **Specific error types** for different failure modes
- **Context preservation** with original error information
- **Graceful degradation** continues with reduced functionality
- **User-friendly messages** explain what went wrong

### Phase 7: Interactive CLI with Tool Discovery

The CLI interface provides comprehensive tool discovery and categorization:

```python
# cli_interface.py - Enhanced CLI with tool discovery
def display_tools_info(tools_count: int, mcp_tool_info: List[Dict[str, Any]]):
    """Display available tools information with categorization."""
    print(f"\n🛠️  Available Tools ({tools_count} total):")
    print("=" * 60)
    
    # Web search tools
    print("\n🔍 Web Search Tools:")
    print("  1. websearch - Search the web to get updated information quickly")
    
    # Categorize MCP tools by server
    for category, tools in categorized_tools.items():
        if tools:
            print(f"\n{category} ({len(tools)} tools):")
            for tool in tools:
                print(f"  • {tool['name']} - {tool['description']}")
```

CLI features:
- **Tool categorization** by functionality (🔍 Web Search, 📚 AWS Docs, ☸️ EKS)
- **Interactive commands** (`tools`, `exit`, natural language)
- **Timeout protection** for agent responses (45 seconds)
- **Graceful error handling** with fallback responses

## Performance Optimizations

### Knowledge-First Strategy
The agent uses an efficiency-optimized approach:

```python
SYSTEM_PROMPT = """You are AWS DevOps bot. Help with AWS infrastructure and operations.

CRITICAL EFFICIENCY RULES:
- Answer from knowledge FIRST before using tools
- Use tools ONLY when you need current/specific data
- MAXIMUM 1 tool call per response
- Keep responses under 300 words
- Be direct and actionable

NON-FUNCTIONAL RULES:
- Be friendly, patient, and understanding with customers
- Always offer additional help after answering questions
- If you can't help with something, direct customers to the appropriate contact
"""
```

### Resource Management
Proper lifecycle management ensures reliability:

```python
# agent.py - Resource management with ExitStack
def main():
    """Main application with proper resource management."""
    try:
        agent, tools_count, mcp_tool_info, mcp_clients = create_agent()
        
        if mcp_clients:
            # Context-managed MCP clients
            with ExitStack() as stack:
                mcp_manager = MCPManager()
                mcp_manager.clients = mcp_clients
                
                if mcp_manager.enter_contexts(stack):
                    run_interactive_loop(agent, tools_count, mcp_tool_info)
                else:
                    run_fallback_loop(agent, tools_count)
        else:
            run_fallback_loop(agent, tools_count)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        app_logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
```

## Testing and Quality Assurance

### Comprehensive Test Suite
The project includes multiple testing approaches:

```python
# tests/test_mcp_usage.py - MCP connectivity testing
def test_mcp_server_connectivity():
    """Test individual MCP server connections."""
    for server_config in MCP_SERVERS:
        result = test_mcp_server(
            server_config['name'],
            server_config['command'],
            server_config['args']
        )
        
        if result['success']:
            print(f"✅ {result['server_name']}: Found {result['tool_count']} tools")
        else:
            print(f"❌ {result['server_name']}: {result['error']}")
```

### Code Quality Metrics
The codebase includes comprehensive quality improvements:

- **Type hints** throughout for better IDE support
- **Docstrings** with Args/Returns documentation
- **Separation of concerns** with modular architecture
- **Error handling** with custom exception hierarchy
- **Logging** with structured, configurable output

## Deployment and Production Readiness

### Dependencies and Installation
```bash
# Core dependencies
pip install strands-agents strands-agents-tools ddgs mcp

# MCP server support
curl -LsSf https://astral.sh/uv/install.sh | sh

# AWS credentials
aws configure
```

### Production Features
- **Signal handlers** for graceful shutdown
- **Structured logging** with configurable levels
- **Configuration validation** at startup
- **Resource cleanup** with context managers
- **Timeout protection** for all external calls

## Key Architectural Decisions

### 1. Modular Design
Each component has a single responsibility:
- `agent.py`: Application orchestration
- `mcp_manager.py`: MCP lifecycle management
- `cli_interface.py`: User interaction
- `websearch_tool.py`: Web search functionality

### 2. Graceful Degradation
The agent works with any combination of available tools:
- **Full functionality**: Web search + 3 MCP servers (21 tools)
- **Partial functionality**: Web search + some MCP servers
- **Minimal functionality**: Web search only (still fully functional)

### 3. Performance-First Approach
- **Temperature 0.3**: Optimized for technical accuracy
- **1 tool call maximum**: Prevents response delays
- **Smart timeouts**: 10s for search, 45s for agent responses
- **Result limiting**: Default 3 search results for speed

## Lessons Learned and Best Practices

### 1. Error Handling is Critical
Custom exceptions with context make debugging significantly easier and provide better user experience.

### 2. Resource Management Matters
Proper context management and cleanup prevent resource leaks and ensure reliability.

### 3. Configuration Validation Saves Time
Early validation catches configuration errors before they cause runtime failures.

### 4. Modular Architecture Enables Testing
Separation of concerns makes individual components testable and maintainable.

### 5. Performance Optimization is Essential
Knowledge-first approach and tool call limits ensure responsive user experience.

## Future Enhancements

### Planned Improvements
1. **Async Support**: Convert to async/await for better concurrency
2. **Caching Layer**: Cache MCP responses for frequently used queries
3. **Metrics Collection**: Add performance monitoring and analytics
4. **Plugin System**: Dynamic loading of custom tools and extensions
5. **Configuration Files**: Support YAML/JSON configuration files

### Scalability Considerations
- **Lazy loading**: Load MCP tools on-demand
- **Connection pooling**: Reuse MCP connections
- **Response streaming**: Stream long responses for better UX
- **Distributed deployment**: Support for multiple agent instances

## Conclusion

Building a production-ready AI agent requires careful attention to architecture, error handling, performance, and user experience. This AWS DevOps Strands Agent demonstrates how to:

- **Integrate multiple data sources** seamlessly (web search + AWS documentation + EKS management)
- **Handle failures gracefully** with comprehensive error handling
- **Optimize for performance** with smart timeouts and result limiting
- **Maintain code quality** with type hints, documentation, and testing
- **Ensure production readiness** with proper resource management and logging

The result is a robust, efficient, and maintainable AI agent that provides comprehensive AWS DevOps assistance while maintaining excellent performance and reliability.

The complete source code and documentation are available, demonstrating modern Python development practices and production-ready AI agent architecture.

---

*Built with ❤️ using Strands Agents Framework, AWS Bedrock, and Claude Sonnet 4*
Kiro: Build a single page technical blog explaining the build process of this Strands agent