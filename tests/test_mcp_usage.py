#!/usr/bin/env python3
"""
Test MCP server connectivity and tool availability.

This script tests all configured MCP servers or a specific server by name.
Usage:
    python test_mcp_usage.py              # Test all servers
    python test_mcp_usage.py <server_name> # Test specific server
"""

import os
import sys
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.mcp_utils import test_mcp_server, MCP_SERVERS

# Set AWS region
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


def display_test_results(results: Dict[str, any]) -> None:
    """Display formatted test results with enhanced information."""
    server_name = results['server_name']
    
    if results['success']:
        tool_count = results['tool_count']
        print(f"✅ {server_name}: Found {tool_count} tools")
        
        if tool_count == 0:
            print("  ⚠️  Warning: Server connected but no tools available")
            return
        
        # Show first 5 tools with better formatting
        max_display = min(5, tool_count)
        for i, tool in enumerate(results['tools'][:max_display], 1):
            tool_name = tool.get('name', 'Unknown')
            print(f"  {i:2d}. {tool_name}")
        
        if tool_count > max_display:
            print(f"  ... and {tool_count - max_display} more tools")
        
        # Find cluster-related tools for EKS server
        if 'EKS' in server_name.upper():
            cluster_tools = [
                tool for tool in results['tools'] 
                if 'cluster' in tool.get('name', '').lower()
            ]
            if cluster_tools:
                print(f"\n🎯 Found {len(cluster_tools)} cluster-related tools:")
                for tool in cluster_tools[:3]:  # Limit display
                    print(f"  - {tool['name']}")
                if len(cluster_tools) > 3:
                    print(f"  ... and {len(cluster_tools) - 3} more cluster tools")
            else:
                print("\n❌ No cluster-related tools found")
    else:
        error_msg = results.get('error', 'Unknown error')
        print(f"❌ {server_name}: {error_msg}")
        
        # Provide helpful hints based on error type
        if 'not found' in error_msg.lower():
            print("💡 Hint: Install uvx with 'curl -LsSf https://astral.sh/uv/install.sh | sh'")
        elif 'connection' in error_msg.lower():
            print("💡 Hint: Check internet connection and server availability")


def test_specific_server(server_name: str) -> bool:
    """Test a specific MCP server by name.
    
    Args:
        server_name: Name of the server to test
        
    Returns:
        True if test passed, False otherwise
    """
    server_config = next(
        (s for s in MCP_SERVERS if s['name'] == server_name), 
        None
    )
    
    if not server_config:
        print(f"❌ Server '{server_name}' not found in configuration")
        print(f"Available servers: {', '.join(s['name'] for s in MCP_SERVERS)}")
        return False
    
    print(f"Testing {server_name} MCP server...")
    results = test_mcp_server(
        server_config['name'],
        server_config['command'],
        server_config['args']
    )
    display_test_results(results)
    return results['success']


def test_all_servers() -> Dict[str, bool]:
    """Test all configured MCP servers.
    
    Returns:
        Dictionary mapping server names to test results
    """
    print("Testing all MCP servers...\n")
    
    results = {}
    for server_config in MCP_SERVERS:
        test_result = test_mcp_server(
            server_config['name'],
            server_config['command'],
            server_config['args']
        )
        display_test_results(test_result)
        results[server_config['name']] = test_result['success']
        print()  # Add spacing between servers
    
    return results


def main() -> None:
    """Main test function with proper exit codes."""
    if len(sys.argv) > 1:
        # Test specific server
        server_name = sys.argv[1]
        success = test_specific_server(server_name)
        sys.exit(0 if success else 1)
    else:
        # Test all servers
        results = test_all_servers()
        
        # Summary
        total_servers = len(results)
        passed_servers = sum(results.values())
        
        print("="*50)
        print("SUMMARY:")
        print(f"Servers tested: {total_servers}")
        print(f"Servers passed: {passed_servers}")
        print(f"Success rate: {passed_servers/total_servers*100:.1f}%")
        
        if passed_servers == total_servers:
            print("🎉 All MCP servers are working correctly!")
        else:
            failed_servers = [name for name, success in results.items() if not success]
            print(f"❌ Failed servers: {', '.join(failed_servers)}")
        
        sys.exit(0 if passed_servers == total_servers else 1)


if __name__ == "__main__":
    main()