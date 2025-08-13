#!/usr/bin/env python3
"""
MCP Manager for handling MCP client lifecycle and tool loading.
"""

from contextlib import ExitStack
from typing import List, Dict, Any, Tuple
from mcp_utils import MCP_SERVERS, create_mcp_client, get_tool_info


class MCPManager:
    """Manages MCP clients and tool loading with proper lifecycle management."""
    
    def __init__(self, lazy_load: bool = False):
        self.clients = []
        self.tool_info = []
        self.tools = []
        self.lazy_load = lazy_load
        self._loaded_servers = set()
    
    def load_mcp_tools(self) -> Tuple[List, List[Dict[str, Any]], List]:
        """
        Load tools from all configured MCP servers.
        
        Returns:
            Tuple of (tools, tool_info, clients)
        """
        if self.lazy_load:
            return self._load_tools_lazy()
        return self._load_tools_eager()
    
    def _load_tools_eager(self) -> Tuple[List, List[Dict[str, Any]], List]:
        """Load all tools immediately."""
        return self._load_servers(MCP_SERVERS)
    
    def _load_tools_lazy(self) -> Tuple[List, List[Dict[str, Any]], List]:
        """Load tools on-demand (placeholder for future enhancement)."""
        # For now, just load eagerly - can be enhanced later
        return self._load_tools_eager()
    
    def _load_servers(self, server_configs: List[Dict]) -> Tuple[List, List[Dict[str, Any]], List]:
        """Load tools from specified server configurations."""
        for server_config in server_configs:
            try:
                client = create_mcp_client(
                    server_config["command"], 
                    server_config["args"],
                    server_config.get("env")
                )
                
                # Get tools from the MCP server within context manager
                with client:
                    mcp_tools = client.list_tools_sync()
                    print(f"📋 {server_config['name']} loaded {len(mcp_tools)} tools")
                    
                    # Store tool information for display
                    for tool in mcp_tools:
                        tool_info = get_tool_info(tool)
                        self.tool_info.append({
                            'server': server_config['name'],
                            'name': tool_info['name'],
                            'description': tool_info['description']
                        })
                    
                    self.tools.extend(mcp_tools)
                    print(f"✅ {server_config['name']} MCP server tools loaded successfully")
                
                # Keep client for runtime usage
                self.clients.append(client)
                
            except ConnectionError as e:
                print(f"⚠️  Connection Error: Could not connect to {server_config['name']}: {e}")
            except ImportError as e:
                print(f"⚠️  Import Error: Missing dependency for {server_config['name']}: {e}")
                self._print_installation_help()
            except Exception as e:
                print(f"⚠️  Warning: Could not load {server_config['name']} tools: {e}")
        
        return self.tools, self.tool_info, self.clients
    
    def _print_installation_help(self):
        """Print installation help for MCP dependencies."""
        print("📝 To enable MCP servers:")
        print("   1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   2. Ensure uvx is in your PATH")
    
    def enter_contexts(self, stack: ExitStack) -> bool:
        """
        Enter all MCP client contexts using the provided ExitStack.
        
        Args:
            stack: ExitStack to manage contexts
            
        Returns:
            True if all contexts entered successfully, False otherwise
        """
        if not self.clients:
            return False
            
        print(f"🔗 Managing {len(self.clients)} MCP client contexts...")
        
        for i, client in enumerate(self.clients):
            try:
                stack.enter_context(client)
                print(f"✅ MCP client {i+1} context entered successfully")
            except Exception as e:
                print(f"❌ Failed to enter MCP client {i+1} context: {e}")
                return False
        
        return True