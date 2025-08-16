# Import Agent and tools
import logging
from contextlib import ExitStack

from strands.agent import Agent
from strands.models.bedrock import BedrockModel

# Import local modules
from config.config import MODEL_ID, MODEL_TEMPERATURE, SYSTEM_PROMPT
from tools.websearch_tool import websearch
from core.mcp_manager import MCPManager
from interfaces.cli_interface import run_interactive_loop, run_fallback_loop

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)


def create_agent() -> tuple[Agent, int, list, list]:
    """
    Create and configure the agent with all available tools.
    
    Returns:
        Tuple of (agent, tools_count, mcp_tool_info, mcp_clients)
    """
    # Create a Bedrock model instance with temperature control
    model = BedrockModel(model_id=MODEL_ID, temperature=MODEL_TEMPERATURE)
    
    # Initialize tools list with websearch
    tools = [websearch]
    
    # Load MCP tools
    mcp_manager = MCPManager()
    mcp_tools, mcp_tool_info, mcp_clients = mcp_manager.load_mcp_tools()
    tools.extend(mcp_tools)
    
    # Create the agent with available tools
    agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=tools)
    
    return agent, len(tools), mcp_tool_info, mcp_clients


def main():
    """Main application entry point with proper resource management."""
    import signal
    import sys
    from core.logger import app_logger
    
    def signal_handler(signum, frame):
        """Handle graceful shutdown on SIGINT/SIGTERM."""
        app_logger.info("Received shutdown signal, cleaning up...")
        print("\n👋 Shutting down gracefully...")
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        agent, tools_count, mcp_tool_info, mcp_clients = create_agent()
        
        # Run the agent in a loop for interactive conversation
        if mcp_clients:
            # Use context managers for all MCP clients
            with ExitStack() as stack:
                mcp_manager = MCPManager()
                mcp_manager.clients = mcp_clients
                
                if mcp_manager.enter_contexts(stack):
                    print("🚀 Starting interactive loop with active MCP contexts...")
                    run_interactive_loop(agent, tools_count, mcp_tool_info)
                else:
                    print("⚠️  Failed to enter MCP contexts, falling back to web search only")
                    run_fallback_loop(agent, tools_count)
        else:
            # Run without MCP clients (web search only)
            run_fallback_loop(agent, tools_count)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        app_logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()