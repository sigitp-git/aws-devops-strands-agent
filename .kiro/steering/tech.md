# Technology Stack

## Core Framework
- **Strands Agents**: Primary agent framework with enhanced architecture
- **AWS Bedrock**: Claude Sonnet 4 model hosting
- **Python 3.10+**: Runtime environment with full type hints

## Dependencies
- `strands-agents`: Core agent framework
- `strands-agents-tools`: Additional agent tools  
- `ddgs`: DuckDuckGo search integration
- `mcp`: Model Context Protocol for AWS documentation access
- `boto3`: AWS SDK (implicit dependency)
- `uv`/`uvx`: Python package manager for MCP server execution

## AWS Services
- **AWS Bedrock**: Model hosting (us-east-1 region)
- **AWS IAM**: Authentication and authorization
- **Claude Sonnet 4**: Model ID `us.anthropic.claude-sonnet-4-20250514-v1:0`

## MCP Integration
- **Protocol**: Model Context Protocol for comprehensive AWS access
- **Servers**: 
  - `awslabs.aws-documentation-mcp-server@latest` (AWS Documentation)
  - `mcp-proxy` with `https://knowledge-mcp.global.api.aws` (AWS Knowledge)
  - `awslabs.eks-mcp-server@latest` (AWS EKS)
- **Transport**: stdio via uvx command execution
- **Purpose**: Real-time AWS documentation, knowledge base, and EKS cluster access
- **Tools**: 21 total tools (1 websearch + 3 AWS docs + 3 AWS knowledge + 14 EKS tools)

## Configuration
- **Temperature**: 0.3 (optimized for technical accuracy with validation)
- **Region**: us-east-1 (configurable via AWS_DEFAULT_REGION)
- **Logging**: Structured logging with multiple loggers (app, mcp, cli)
- **Error Handling**: Custom exception hierarchy for better debugging
- **Resource Management**: Proper cleanup with signal handlers

## Common Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install uv for MCP server support
curl -LsSf https://astral.sh/uv/install.sh | sh

# Configure AWS credentials
aws configure
```

### Development
```bash
# Run the agent
python3 agent.py

# Check available Bedrock models
aws bedrock list-foundation-models --region us-east-1 --output json | grep sonnet
```

### Testing
- Interactive testing via command-line interface
- Type 'tools' to see all available capabilities
- Type 'exit' to quit the agent session
- Built-in tool discovery and categorization