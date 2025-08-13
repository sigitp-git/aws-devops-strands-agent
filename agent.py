# Import Agent and tools
import logging
from contextlib import ExitStack

from strands.agent import Agent
from strands.models.bedrock import BedrockModel

# Import local modules
from config import MODEL_ID, MODEL_TEMPERATURE, SYSTEM_PROMPT
from websearch_tool import websearch
from mcp_utils import MCP_SERVERS, create_mcp_client, get_tool_info
from cli_interface import run_interactive_loop, run_fallback_loop

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)


# Create a Bedrock model instance with temperature control
model = BedrockModel(model_id=MODEL_ID, temperature=MODEL_TEMPERATURE)

# Initialize tools list with websearch
tools = [websearch]



# Try to connect to MCP servers and add AWS tools
mcp_clients = []
mcp_tool_info = []  # Store MCP tool information for display

for server_config in MCP_SERVERS:
    try:
        client = create_mcp_client(
            server_config["command"], 
            server_config["args"],
            server_config.get("env")
        )
        
        # Get the tools from the MCP server within context manager
        with client:
            mcp_tools = client.list_tools_sync()
            print(f"📋 {server_config['name']} loaded {len(mcp_tools)} tools")
            
            # Store tool information for later display
            for tool in mcp_tools:
                tool_info = get_tool_info(tool)
                mcp_tool_info.append({
                    'server': server_config['name'],
                    'name': tool_info['name'],
                    'description': tool_info['description']
                })
            
            tools.extend(mcp_tools)
            print(f"✅ {server_config['name']} MCP server tools loaded successfully")
        
        # Keep client for runtime usage - will be re-entered in main loop
        mcp_clients.append(client)
            
    except ConnectionError as e:
        print(f"⚠️  Connection Error: Could not connect to {server_config['name']}: {e}")
    except ImportError as e:
        print(f"⚠️  Import Error: Missing dependency for {server_config['name']}: {e}")
        print("📝 To enable MCP servers:")
        print("   1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   2. Ensure uvx is in your PATH")
    except Exception as e:
        print(f"⚠️  Warning: Could not load {server_config['name']} tools: {e}")

# Create the agent with available tools
agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=tools)


if __name__ == "__main__":
    # Run the agent in a loop for interactive conversation
    # Keep MCP clients alive during the conversation
    if mcp_clients:
        print(f"🔗 Managing {len(mcp_clients)} MCP client contexts...")
        # Use context managers for all MCP clients
        with ExitStack() as stack:
            # Enter all MCP client contexts
            for i, client in enumerate(mcp_clients):
                try:
                    stack.enter_context(client)
                    print(f"✅ MCP client {i+1} context entered successfully")
                except Exception as e:
                    print(f"❌ Failed to enter MCP client {i+1} context: {e}")
            
            # Run the interactive loop with MCP tools
            print("🚀 Starting interactive loop with active MCP contexts...")
            run_interactive_loop(agent, len(tools), mcp_tool_info)
    else:
        # Run without MCP clients (web search only)
        run_fallback_loop(agent, len(tools))