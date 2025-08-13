# Import Agent and tools
import logging
import os

from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException
from strands.agent import Agent
from strands.tools import tool
from strands.models.bedrock import BedrockModel
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

# Set AWS region
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# Configure logging
logging.getLogger("strands").setLevel(
    logging.INFO
)  # Set to DEBUG for more detailed logs


# Define a websearch tool using DuckDuckGoSearch SDK with timeout protection
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


# Create a Bedrock model instance with temperature control
# Temperature 0.3: Focused and consistent responses, ideal for technical accuracy
# Adjust temperature: 0.1-0.3 (very focused), 0.4-0.7 (balanced), 0.8-1.0 (creative)
model = BedrockModel(
    model_id='us.anthropic.claude-sonnet-4-20250514-v1:0', 
    temperature=0.3
)

# Initialize tools list with websearch
tools = [websearch]

# MCP servers configuration
# All three MCP servers enabled for comprehensive AWS knowledge and capabilities
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
                        # Get first line of description for brevity
                        full_desc = tool.tool_spec.description
                        tool_desc = full_desc.split('\n')[0].strip()
                        if len(tool_desc) > 100:
                            tool_desc = tool_desc[:97] + "..."
                    elif isinstance(tool.tool_spec, dict) and 'description' in tool.tool_spec:
                        full_desc = tool.tool_spec['description']
                        tool_desc = full_desc.split('\n')[0].strip()
                        if len(tool_desc) > 100:
                            tool_desc = tool_desc[:97] + "..."
                
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


if __name__ == "__main__":
    print("\n🚀 AWS-DevOps-bot: Ask me about DevOps on AWS!")
    print("💡 Type 'tools' to see available capabilities, or 'exit' to quit.\n")

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
                if not user_input.strip():
                    print("\nAWS-DevOps-bot > Please ask me something about DevOps on AWS!")
                    continue
                
                # Special command to list available tools
                if user_input.lower() in ["list tools", "show tools", "available tools", "what tools", "tools"]:
                    print(f"\n🛠️  Available Tools ({len(tools)} total):")
                    print("=" * 60)
                    
                    # Show websearch tool first
                    print("\n🔍 Web Search Tools:")
                    print("  1. websearch - Search the web to get updated information quickly")
                    
                    # Group MCP tools by server
                    aws_doc_tools = []
                    aws_knowledge_tools = []
                    aws_eks_tools = []
                    
                    for tool_info in mcp_tool_info:
                        server = tool_info['server']
                        name = tool_info['name']
                        desc = tool_info['description']
                        
                        # Truncate long descriptions
                        if len(desc) > 80:
                            desc = desc[:77] + "..."
                        
                        tool_entry = f"  • {name} - {desc}"
                        
                        if 'Documentation' in server:
                            aws_doc_tools.append(tool_entry)
                        elif 'Knowledge' in server:
                            aws_knowledge_tools.append(tool_entry)
                        elif 'EKS' in server:
                            aws_eks_tools.append(tool_entry)
                    
                    # Display MCP tools by category
                    if aws_doc_tools:
                        print(f"\n📚 AWS Documentation Tools ({len(aws_doc_tools)} tools):")
                        for tool in aws_doc_tools:
                            print(tool)
                    
                    if aws_knowledge_tools:
                        print(f"\n🧠 AWS Knowledge Tools ({len(aws_knowledge_tools)} tools):")
                        for tool in aws_knowledge_tools:
                            print(tool)
                    
                    if aws_eks_tools:
                        print(f"\n☸️  AWS EKS Tools ({len(aws_eks_tools)} tools):")
                        for tool in aws_eks_tools:
                            print(tool)
                    
                    print("\n💡 You can ask me to use any of these tools or just ask questions naturally!")
                    print("🎯 Example: 'Use AWS Documentation to find S3 pricing' or 'List my EKS clusters'")
                    continue
                
                # Add timeout protection for agent calls
                import signal
                def timeout_handler(signum, frame):
                    raise TimeoutError("Agent response timeout after 30 seconds")
                
                try:
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(30)  # 30 second timeout
                    print("🤖 Processing your request...")
                    response = agent(user_input)
                    signal.alarm(0)  # Cancel timeout
                    print(f"\nAWS-DevOps-bot > {response}")
                except TimeoutError:
                    signal.alarm(0)
                    print(f"\nAWS-DevOps-bot > I apologize, but that request took too long to process. Let me provide a quick response based on my knowledge instead.")
                    print("For EKS cluster operations, you can use: `aws eks list-clusters` or check the AWS Console.")
                except Exception as e:
                    signal.alarm(0)
                    print(f"\nAWS-DevOps-bot > I encountered an error: {e}. Let me help you with general AWS DevOps guidance instead.")
                finally:
                    signal.alarm(0)
    else:
        # Run without MCP clients (web search only)
        while True:
            user_input = input("\nYou > ")
            if user_input.lower() == "exit":
                print("Happy DevOpsing!")
                break
            if not user_input.strip():
                print("\nAWS-DevOps-bot > Please ask me something about DevOps on AWS!")
                continue
            
            # Special command to list available tools
            if user_input.lower() in ["list tools", "show tools", "available tools", "what tools", "tools"]:
                print(f"\n🛠️  Available Tools ({len(tools)} total):")
                print("=" * 50)
                print("\n🔍 Web Search Tools:")
                print("  1. websearch - Search the web to get updated information quickly.")
                print("\n⚠️  Note: MCP servers (AWS Documentation, Knowledge, EKS) are not available.")
                print("💡 You can still ask me AWS DevOps questions and I'll help with my built-in knowledge!")
                continue
            
            # Add timeout protection for agent calls
            import signal
            def timeout_handler(signum, frame):
                raise TimeoutError("Agent response timeout after 30 seconds")
            
            try:
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(30)  # 30 second timeout
                print("🤖 Processing your request...")
                response = agent(user_input)
                signal.alarm(0)  # Cancel timeout
                print(f"\nAWS-DevOps-bot > {response}")
            except TimeoutError:
                signal.alarm(0)
                print(f"\nAWS-DevOps-bot > I apologize, but that request took too long to process. Let me provide a quick response based on my knowledge instead.")
            except Exception as e:
                signal.alarm(0)
                print(f"\nAWS-DevOps-bot > I encountered an error: {e}. Let me help you with general AWS DevOps guidance instead.")
            finally:
                signal.alarm(0)