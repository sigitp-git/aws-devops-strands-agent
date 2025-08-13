# AWS DevOps Strands Agent

An intelligent AWS DevOps assistant bot built with the Strands Agents framework, powered by Claude Sonnet 4 on AWS Bedrock with web search capabilities.

## Features

- **AI-Powered Assistant**: Uses Claude Sonnet 4 model via AWS Bedrock for intelligent responses
- **Dual Information Sources**: Combines web search (DuckDuckGo SDK) with direct AWS documentation access
- **Triple MCP Integration**: Real-time AWS documentation, knowledge base, and EKS cluster access via Model Context Protocol with dynamic tool loading
- **AWS DevOps Specialization**: Focused on DevOps best practices, CI/CD, IaC, and AWS services
- **Interactive CLI**: Command-line interface with tool discovery and categorization
- **Optimized Configuration**: Temperature setting (0.3) for technical accuracy and consistency
- **Efficiency Optimized**: Smart tool usage with knowledge-first approach and minimal tool calls for faster responses

## Prerequisites

- Python 3.10+
- AWS Account with Bedrock access
- AWS credentials configured
- Claude Sonnet 4 model access in AWS Bedrock
- `uv` and `uvx` installed for MCP server management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sigitp-git/aws-devops-strands-agent.git
cd aws-devops-strands-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure AWS credentials are configured:
```bash
aws configure
```

4. (Optional) Install uv and uvx for enhanced AWS documentation access:
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or via pip: pip install uv
```



**Note**: The bot works perfectly with just web search if MCP tools aren't available. AWS documentation, knowledge base, and EKS management tools are automatically loaded if `uvx` is installed and working.

**Performance**: The agent includes all three MCP servers enabled by default for comprehensive AWS capabilities:
- **AWS Documentation Server**: Fast access to official AWS documentation
- **AWS Knowledge Server**: Comprehensive AWS knowledge base (may be slower but more thorough)
- **AWS EKS Server**: Direct EKS cluster management and Kubernetes operations

All servers are automatically detected and loaded - if one fails, the agent continues with available tools. The agent now stores detailed MCP tool information for enhanced tool discovery and categorization. This provides the most comprehensive AWS DevOps assistance possible while maintaining graceful fallbacks.

## Tool Discovery

The agent includes built-in tool discovery capabilities. Once running, you can use the `tools` command to see all available capabilities:

```bash
You > tools
```

This will display:
- **🔍 Web Search Tools**: DuckDuckGo search with timeout protection
- **📚 AWS Documentation Tools**: Direct AWS documentation access (3 tools)
- **🧠 AWS Knowledge Tools**: AWS knowledge base access (3 tools)  
- **☸️ AWS EKS Tools**: EKS cluster management and Kubernetes operations (14 tools)

Total: 21 tools when all MCP servers are available.

## Usage

Run the AWS DevOps bot:

```bash
python3 agent.py
```

The bot will automatically detect available tools and start an interactive session. You'll see:
- 📋 AWS Documentation loaded X tools
- ✅ AWS Documentation MCP server tools loaded successfully (if uvx is available)
- 📋 AWS Knowledge loaded X tools  
- ✅ AWS Knowledge MCP server tools loaded successfully (if uvx is available)
- 📋 AWS EKS loaded X tools
- ✅ AWS EKS MCP server tools loaded successfully (if uvx is available)
- ⚠️ Warning messages if MCP tools can't be loaded (bot still works with web search)

**Note**: The agent uses proper context management for MCP clients to ensure reliable connections throughout the session.

You can ask questions about:
- AWS DevOps best practices
- CI/CD pipeline setup
- Infrastructure as Code (CloudFormation, CDK)
- Container orchestration (ECS, EKS)
- EKS cluster management and troubleshooting
- Kubernetes workload deployment and monitoring
- Monitoring and observability
- Security best practices
- AWS service configurations
- Real-time AWS documentation queries via MCP integration

### Special Commands

- **`tools`** or **`list tools`**: Display all available tools categorized by type
  - 🔍 Web Search Tools
  - 📚 AWS Documentation Tools  
  - 🧠 AWS Knowledge Tools
  - ☸️ AWS EKS Tools
  - 🔧 Other Tools
- **`exit`**: Quit the interactive session

## Example Interactions

```
🚀 AWS-DevOps-bot: Ask me about DevOps on AWS!
💡 Type 'tools' to see available capabilities, or 'exit' to quit.

You > tools
🛠️  Available Tools (21 total):
============================================================

🔍 Web Search Tools:
  1. websearch - Search the web to get updated information quickly

📚 AWS Documentation Tools (3 tools):
  • read_documentation - Fetch and convert an AWS documentation page to markdown format.
  • search_documentation - Search AWS documentation using the official AWS Documentation Search API.
  • recommend - Get content recommendations for an AWS documentation page.

🧠 AWS Knowledge Tools (3 tools):
  • aws___search_documentation - Search AWS documentation using the official AWS Documentation Search API.
  • aws___read_documentation - Fetch and convert an AWS documentation page to markdown format.
  • aws___recommend - Get content recommendations for an AWS documentation page.

☸️ AWS EKS Tools (14 tools):
  • list_k8s_resources - List Kubernetes resources of a specific kind.
  • get_pod_logs - Get logs from a pod in a Kubernetes cluster.
  • get_k8s_events - Get events related to a specific Kubernetes resource.
  • manage_k8s_resource - Manage a single Kubernetes resource with various operations.
  • apply_yaml - Apply a Kubernetes YAML from a local file.
  [... and 9 more EKS/Kubernetes management tools]

💡 You can ask me to use any of these tools or just ask questions naturally!
🎯 Example: 'Use AWS Documentation to find S3 pricing' or 'List my EKS clusters'

You > aws well architected framework
[Bot provides detailed information about the AWS Well-Architected Framework using both web search and AWS documentation]

You > how to set up ci/cd pipeline with CodePipeline
[Bot provides guidance on setting up CI/CD pipelines with AWS services, accessing real-time documentation]

You > latest EKS best practices
[Bot searches for current best practices and references official AWS documentation]

You > check my EKS cluster status
[Bot can directly interact with your EKS clusters for real-time status and troubleshooting]

You > exit
Happy DevOpsing!
```

## Testing

The project includes comprehensive test scripts in the `tests/` directory:

### Run All Tests
```bash
# Test MCP server connectivity
python3 tests/test_mcp_usage.py

# Test basic agent functionality  
python3 tests/simple_mcp_test.py
```

### Test Specific MCP Servers
```bash
# Test individual servers
python3 tests/test_mcp_usage.py "AWS Documentation"
python3 tests/test_mcp_usage.py "AWS Knowledge"
python3 tests/test_mcp_usage.py "AWS EKS"
```

### Test Output Example
```
✅ AWS Documentation: Found 3 tools
  1. read_documentation
  2. search_documentation  
  3. recommend

✅ AWS EKS: Found 14 tools
  1. get_cloudwatch_logs
  2. get_cloudwatch_metrics
  3. search_eks_troubleshoot_guide
  [... and 11 more tools]
```

See `tests/README.md` for detailed testing documentation.

## Code Quality & Architecture

This project has been enhanced with significant code quality improvements:

### ✅ **Architectural Improvements**
- **Separation of Concerns**: Modular design with dedicated components
- **MCPManager**: Centralized MCP client lifecycle management
- **Custom Exceptions**: Specific error types for better debugging
- **Structured Logging**: Comprehensive logging with configurable levels
- **Resource Management**: Proper cleanup and graceful shutdown

### ✅ **Enhanced Error Handling**
- **Custom Exception Hierarchy**: `MCPConnectionError`, `MCPToolLoadError`, `AgentTimeoutError`, `ConfigurationError`
- **Graceful Degradation**: Application continues with reduced functionality when possible
- **Informative Messages**: Context-aware error messages for better debugging

### ✅ **Developer Experience**
- **Type Hints**: Full type annotations for better IDE support
- **Documentation**: Comprehensive docstrings with Args/Returns
- **Configuration Validation**: Early detection of configuration issues
- **Testing Framework**: Organized test structure with utilities

See `IMPROVEMENTS.md` for detailed technical documentation of all enhancements.

## Performance & Efficiency

The agent is optimized for fast, efficient responses with the following approach:

### Smart Tool Usage Strategy
- **Knowledge-First**: Attempts to answer from built-in knowledge before using external tools
- **Minimal Tool Calls**: Limited to 1-2 tool calls maximum per response to reduce latency
- **Prioritized Tools**: Web search prioritized for speed, AWS documentation tools for specific technical details
- **Graceful Fallbacks**: Always provides helpful responses even if tools are slow or fail
- **Concise Responses**: Focused on delivering actionable information quickly

### Performance Optimizations
- **Enhanced Web Search**: 10-second timeout protection with smart result limiting (default 3 results)
- **Comprehensive MCP Server Support**: All three MCP servers enabled by default:
  - AWS Documentation Server (fast documentation access)
  - AWS Knowledge Server (comprehensive knowledge base)
  - AWS EKS Server (direct cluster management capabilities)
- **Automatic Tool Detection**: Dynamically loads available tools without breaking if some fail
- **Proper Context Management**: MCP clients are properly managed with context managers for reliable connections
- **Error Resilience**: Continues working with available tools even if some MCP servers are unavailable
- **Visual Feedback**: Real-time search progress indicators and result counts

This ensures users get fast, accurate responses while maintaining access to real-time information when needed.

## Configuration

### Web Search Tool
The agent includes a custom websearch tool built with the DuckDuckGo Search SDK with performance optimizations:

```python
@tool
def websearch(
    keywords: str, region: str = "us-en", max_results: int | None = 3
) -> str:
    """Search the web to get updated information quickly.
    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
        max_results (int | None): The maximum number of results to return (default: 3 for speed).
    Returns:
        List of dictionaries with search results.
    """
    import signal
    import time
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Search timeout after 10 seconds")
    
    try:
        # Set timeout for search operation
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)  # 10 second timeout
        
        # Limit results for faster responses
        if max_results is None or max_results > 5:
            max_results = 3
            
        print(f"🔍 Searching for: {keywords}")
        results = DDGS().text(keywords, region=region, max_results=max_results)
        
        # Cancel timeout
        signal.alarm(0)
        
        if results:
            print(f"✅ Found {len(results)} results")
            return results
        else:
            return "No results found."
            
    except TimeoutError:
        signal.alarm(0)
        return "Search timeout - please try a more specific query."
    except RatelimitException:
        return "Rate limit reached - please try again in a moment."
    except DDGSException as d:
        return f"Search service error: {d}"
    except Exception as e:
        return f"Search failed: {e}"
    finally:
        signal.alarm(0)  # Ensure timeout is always cancelled
```

**Enhanced Features:**
- **Timeout Protection**: 10-second timeout prevents hanging searches
- **Speed Optimization**: Default limit of 3 results for faster responses
- **Smart Result Limiting**: Automatically caps results at 5 maximum for performance
- **Visual Feedback**: Progress indicators show search status and result counts (🔍 Searching, ✅ Found X results)
- **Improved Error Handling**: User-friendly error messages for timeouts and rate limits
- **Regional Search Support**: Multiple regions (us-en, uk-en, etc.)
- **Graceful Cleanup**: Ensures timeout signals are always cancelled

### Enhanced MCP Integration
The agent includes Model Context Protocol (MCP) integration for direct access to AWS resources with improved dynamic tool loading and unified execution:

#### Supported MCP Servers:
1. **AWS Documentation Server**: Direct access to AWS documentation (fast)
2. **AWS Knowledge Server**: Access to AWS knowledge base and best practices (comprehensive but slower)
3. **AWS EKS Server**: Direct access to EKS cluster management and operations (requires AWS credentials)
3. **AWS EKS Server**: Direct access to Amazon EKS clusters and Kubernetes resources (requires AWS credentials and EKS access)

```python
# MCP servers configuration in agent.py
mcp_servers = [
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
            "--transport",
            "streamablehttp",
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
        ]
    }
]

# Try to connect to MCP servers and add AWS tools
mcp_clients = []
mcp_tool_info = []  # Store MCP tool information for display

for server_config in mcp_servers:
    try:
        client = MCPClient(lambda config=server_config: stdio_client(
            StdioServerParameters(
                command=config["command"], 
                args=config["args"]
            )
        ))
        
        # Get the tools from the MCP server within context manager
        with client:
            mcp_tools = client.list_tools_sync()
            print(f"📋 {server_config['name']} loaded {len(mcp_tools)} tools")
            
            # Store tool information for later display
            for tool in mcp_tools:
                # Get tool information from the MCP tool attributes
                tool_name = getattr(tool, 'tool_name', 'Unknown Tool')
                tool_desc = 'No description available'
                
                # Try to get description from tool_spec
                if hasattr(tool, 'tool_spec') and tool.tool_spec:
                    if hasattr(tool.tool_spec, 'description'):
                        tool_desc = tool.tool_spec.description
                    elif isinstance(tool.tool_spec, dict) and 'description' in tool.tool_spec:
                        tool_desc = tool.tool_spec['description']
                
                mcp_tool_info.append({
                    'server': server_config['name'],
                    'name': tool_name,
                    'description': tool_desc
                })
            
            tools.extend(mcp_tools)
            print(f"✅ {server_config['name']} MCP server tools loaded successfully")
        
        # Keep client for runtime usage
        mcp_clients.append(client)
            
    except Exception as e:
        print(f"⚠️  Warning: Could not load {server_config['name']} tools: {e}")
        print("📝 To enable MCP servers:")
        print("   1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   2. Ensure uvx is in your PATH")

# Create the agent with available tools
agent = Agent(
    model=model,
    system_prompt="""You are AWS DevOps bot, a helpful devops assistant for Amazon Web Services (AWS) environment.
    Help users find AWS DevOps best practices and answer questions related to AWS infrastructure development and operations.
    
    CRITICAL EFFICIENCY GUIDELINES:
    - ALWAYS provide a helpful response from your knowledge base first
    - Use tools ONLY when you need very specific, current information that you don't already know
    - NEVER use more than 1 tool call per response to prevent delays
    - If a tool fails or is slow, continue with your built-in knowledge
    - For questions about AWS services, versions, or general information, answer directly without tools
    - Only use tools for very specific technical details, current pricing, or recent updates
    - Keep responses concise and actionable""",
    tools=tools,
)
```

**Enhanced Dynamic Tool Loading**: The agent automatically detects and loads available tools with improved architecture:
- Always includes: DuckDuckGo web search via DDGS SDK
- Conditionally includes: AWS documentation and EKS management MCP tools (if uvx is available)
- Graceful fallback: Works perfectly with web search only if MCP tools fail to load
- Unified execution: Single execution loop handles all tool combinations seamlessly
- Improved error handling: Clear installation guidance when MCP tools aren't available
- Proper client lifecycle management: MCP clients are preserved for runtime usage with proper context management
- Context manager integration: Uses ExitStack to manage multiple MCP client contexts reliably
- Triple MCP server support: AWS Documentation, AWS Knowledge, and AWS EKS servers for comprehensive coverage
- Streamlined tool information storage: Clean MCP tool metadata extraction using getattr() and tool_spec attributes for better categorization and display
- Clean console output: Shows tool count without verbose tool name listings for better readability

### EKS Management Capabilities

With the AWS EKS MCP server integration, the agent can:

**Cluster Operations:**
- List and describe EKS clusters
- Check cluster status and health
- Manage cluster configurations
- Monitor cluster resources and utilization

**Workload Management:**
- Deploy and manage Kubernetes applications
- Troubleshoot pod and service issues
- Monitor workload performance
- Access logs and events

**Security & Compliance:**
- Review security configurations
- Check IAM roles and policies
- Validate network policies
- Monitor compliance status

**Note**: EKS operations require appropriate AWS permissions and may modify cluster resources when using write operations.

**Runtime Execution with Context Management:**
The agent uses proper context management for MCP clients during the interactive session:

```python
# Run the agent in a loop for interactive conversation
# Keep MCP clients alive during the conversation
if mcp_clients:
    # Use context managers for all MCP clients
    from contextlib import ExitStack
    with ExitStack() as stack:
        # Enter all MCP client contexts
        for client in mcp_clients:
            stack.enter_context(client)
        
        # Run the interactive loop
        while True:
            user_input = input("\nYou > ")
            if user_input.lower() == "exit":
                print("Happy DevOpsing!")
                break
            # ... rest of interactive loop
```

This provides:
- Real-time access to AWS documentation
- Up-to-date service information via AWS Knowledge MCP proxy
- Direct EKS cluster management and troubleshooting capabilities
- Enhanced accuracy for AWS-specific queries
- Seamless integration between web search and AWS documentation
- Robust fallback mechanism with unified execution model
- Simplified architecture for better maintainability
- Reliable MCP client lifecycle management with proper context handling
- Persistent MCP connections throughout the interactive session

### Model Temperature
The bot uses a temperature setting of 0.3 for optimal balance between accuracy and engagement:
- **0.1-0.3**: Very focused, ideal for technical accuracy
- **0.4-0.7**: Balanced responses
- **0.8-1.0**: More creative responses

You can adjust the temperature in `agent.py`:
```python
model = BedrockModel(
    model_id='us.anthropic.claude-sonnet-4-20250514-v1:0', 
    temperature=0.3  # Adjust this value
)
```

## Project Structure

```
aws-devops-strands-agent/
├── agent.py              # Main application orchestration with improved architecture
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
├── tests/               # Test scripts and utilities
│   ├── README.md        # Testing documentation
│   ├── test_mcp_usage.py # MCP server connectivity tests
│   └── simple_mcp_test.py # Basic functionality tests
├── .kiro/               # Kiro IDE configuration
│   └── steering/        # AI assistant steering rules
│       ├── structure.md # Project structure guidelines
│       ├── tech.md      # Technology stack information
│       └── product.md   # Product overview
└── README.md            # This file
```

## Dependencies

Core Python packages (installed via `pip install -r requirements.txt`):
- `strands-agents`: Core agent framework
- `strands-agents-tools`: Additional agent tools and MCP integration
- `ddgs`: DuckDuckGo search SDK integration
- `mcp`: Model Context Protocol for AWS documentation access

External tools (optional, for enhanced AWS capabilities):
- `uv` and `uvx`: Python package manager for MCP server execution
- AWS CLI: For credential configuration and verification

## AWS Services Used

- **AWS Bedrock**: Claude Sonnet 4 model hosting
- **AWS IAM**: Authentication and authorization
- **AWS Regions**: us-east-1 (configurable)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Troubleshooting

### Common Issues

**"Could not load AWS [Server] tools" warnings:**
- This is normal if `uvx` isn't installed or MCP servers can't connect
- The bot will work perfectly with web search only
- To enable all MCP servers: install `uv` and ensure `uvx` is in your PATH
- Use the `tools` command in the agent to see which tools are actually loaded

**AWS Bedrock access errors:**
- Verify AWS credentials: `aws sts get-caller-identity`
- Check Bedrock model access in your AWS region
- Ensure you have proper IAM permissions for Bedrock

**Import errors:**
- Run: `pip install -r requirements.txt`
- Check Python version (3.10+ required)

**Slow response times:**
- All three MCP servers are enabled by default for comprehensive coverage
- The AWS Knowledge MCP server can be slower than AWS Documentation server but provides more thorough information
- EKS operations may take longer due to cluster API calls but enable direct cluster management
- **Agent is optimized with CRITICAL EFFICIENCY GUIDELINES**: Limited to maximum 1 tool call per response to prevent delays
- **Knowledge-first approach**: Agent provides responses from built-in knowledge before using external tools
- **Enhanced web search**: 10-second timeout protection with smart result limiting (default 3 results)
- **Enhanced tool discovery**: MCP tool information is stored and categorized for better user experience
- **Clean console output**: Tool loading shows count without verbose listings for better performance
- **Proper context management**: MCP clients use ExitStack for reliable connection handling
- If responses are consistently slow, you can disable specific servers by commenting them out in the `mcp_servers` list in `agent.py`
- Web search (DuckDuckGo) is prioritized for speed when possible

**EKS permission errors:**
- Ensure your AWS credentials have EKS permissions
- Check that your IAM user/role can access the target EKS clusters
- Verify cluster exists and is accessible in your configured region

### Testing

Test the agent and verify MCP integration:
```bash
python3 agent.py
```

Then use the `tools` command to see all loaded capabilities:
```bash
You > tools
```

This will show you exactly which MCP servers loaded successfully and what tools are available.

## Support

For issues and questions:
- Open an issue on GitHub
- Check AWS Bedrock documentation for model access
- Verify AWS credentials and permissions

---

Built with ❤️ using Strands Agents and AWS Bedrock