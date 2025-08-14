#!/usr/bin/env python3
"""
Simple test to verify MCP agent functionality.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Configuration constants
MCP_COMMAND = 'uvx'
MCP_SERVER = 'awslabs.aws-documentation-mcp-server@latest'
TEST_QUERY = "What is AWS S3?"
RESPONSE_PREVIEW_LENGTH = 200

try:
    from config import MODEL_ID, MODEL_TEMPERATURE, SYSTEM_PROMPT
    from websearch_tool import websearch
    from strands.agent import Agent
    from strands.models.bedrock import BedrockModel
    from mcp_utils import create_mcp_client
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed and config files exist.")
    sys.exit(1)


def test_websearch_agent() -> bool:
    """Test agent with websearch tool only."""
    print("Testing agent with websearch only...")
    try:
        model = BedrockModel(model_id=MODEL_ID, temperature=MODEL_TEMPERATURE)
        agent = Agent(model=model, system_prompt=SYSTEM_PROMPT, tools=[websearch])
        
        response = agent(TEST_QUERY)
        print("✅ SUCCESS! Agent works with websearch:")
        # Handle AgentResult object properly
        response_text = response.content if hasattr(response, 'content') else str(response)
        preview = response_text[:RESPONSE_PREVIEW_LENGTH] + "..." if len(response_text) > RESPONSE_PREVIEW_LENGTH else response_text
        print(preview)
        return True
        
    except ImportError as e:
        print(f"❌ Import error - missing dependency: {e}")
        return False
    except Exception as e:
        print(f"❌ Websearch test failed: {type(e).__name__}: {e}")
        return False


def test_mcp_connection() -> bool:
    """Test MCP server connection and tool loading."""
    print("Testing AWS Documentation MCP server connection...")
    try:
        client = create_mcp_client(MCP_COMMAND, [MCP_SERVER])
        
        with client:
            mcp_tools = client.list_tools_sync()
            print(f"✅ Successfully loaded {len(mcp_tools)} MCP tools")
            
            # List the tools with better formatting
            for i, tool in enumerate(mcp_tools, 1):
                tool_name = getattr(tool, 'tool_name', 'Unknown')
                print(f"  {i:2d}. {tool_name}")
        
        print("✅ MCP server connection works!")
        return True
        
    except ConnectionError as e:
        print(f"❌ Connection error - check network/MCP server: {e}")
        return False
    except Exception as e:
        print(f"❌ MCP connection failed: {type(e).__name__}: {e}")
        return False


def main():
    """Main test execution with summary reporting."""
    print("🧪 Simple MCP Test - Testing agent with just websearch first...")
    
    # Run tests
    websearch_success = test_websearch_agent()
    
    print("\n" + "="*50)
    print("Now testing if the issue is with MCP tools...")
    
    mcp_success = test_mcp_connection()
    
    # Summary report
    print("\n" + "="*50)
    print("TEST SUMMARY:")
    print(f"Websearch Agent: {'✅ PASS' if websearch_success else '❌ FAIL'}")
    print(f"MCP Connection:  {'✅ PASS' if mcp_success else '❌ FAIL'}")
    
    passed_tests = sum([websearch_success, mcp_success])
    print(f"\nResults: {passed_tests}/2 tests passed")
    
    if websearch_success and mcp_success:
        print("\n🎉 All tests passed! The agent is working correctly.")
    elif websearch_success and not mcp_success:
        print("\n🔍 Websearch works but MCP fails. Check MCP server setup.")
    elif not websearch_success:
        print("\n⚠️  Basic agent functionality failed. Check configuration.")
        print("💡 Verify AWS credentials and Bedrock model access")


if __name__ == "__main__":
    main()