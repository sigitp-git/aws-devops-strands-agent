#!/usr/bin/env python3
"""
MCP utility functions for AWS DevOps agent.
"""

import os
from typing import List, Dict, Any, Optional
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

# Constants
DEFAULT_DESCRIPTION_MAX_LENGTH = 100
DESCRIPTION_TRUNCATE_SUFFIX = "..."


def create_mcp_client(command: str, args: List[str], env: Optional[Dict[str, str]] = None) -> MCPClient:
    """
    Create an MCP client with standardized configuration.
    
    Args:
        command: Command to execute (e.g., "uvx")
        args: Arguments for the command
        env: Optional environment variables to pass to the server
        
    Returns:
        Configured MCPClient instance
        
    Raises:
        ConnectionError: If client cannot be created
        FileNotFoundError: If command is not found
        PermissionError: If insufficient permissions
    """
    try:
        # Merge environment variables
        server_env = os.environ.copy()
        if env:
            server_env.update(env)
            
        return MCPClient(lambda: stdio_client(
            StdioServerParameters(command=command, args=args, env=server_env)
        ))
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Command '{command}' not found. Ensure it's installed and in PATH: {e}")
    except PermissionError as e:
        raise PermissionError(f"Permission denied executing '{command}': {e}")
    except Exception as e:
        raise ConnectionError(f"Failed to create MCP client: {e}")


def _truncate_description(description: str, max_length: int = DEFAULT_DESCRIPTION_MAX_LENGTH) -> str:
    """Truncate description to specified length with ellipsis."""
    if len(description) > max_length:
        return description[:max_length - len(DESCRIPTION_TRUNCATE_SUFFIX)] + DESCRIPTION_TRUNCATE_SUFFIX
    return description


def _extract_description_from_spec(tool_spec) -> str:
    """Extract description from tool spec, handling different formats."""
    if hasattr(tool_spec, 'description'):
        return tool_spec.description.split('\n')[0].strip()
    elif isinstance(tool_spec, dict) and 'description' in tool_spec:
        return tool_spec['description'].split('\n')[0].strip()
    return 'No description available'


def get_tool_info(tool) -> Dict[str, str]:
    """
    Extract tool information in a standardized format.
    
    Args:
        tool: MCP tool object
        
    Returns:
        Dictionary with tool name and description
    """
    tool_name = getattr(tool, 'tool_name', 'Unknown Tool')
    tool_desc = 'No description available'
    
    # Try to get description from tool_spec
    if hasattr(tool, 'tool_spec') and tool.tool_spec:
        full_desc = _extract_description_from_spec(tool.tool_spec)
        tool_desc = _truncate_description(full_desc)
    
    return {
        'name': tool_name,
        'description': tool_desc
    }


def test_mcp_server(server_name: str, command: str, args: List[str]) -> Dict[str, Any]:
    """
    Test MCP server connectivity and return tool information.
    
    Args:
        server_name: Human-readable server name
        command: Command to execute
        args: Arguments for the command
        
    Returns:
        Dictionary with test results and tool information
    """
    result = {
        'server_name': server_name,
        'success': False,
        'tools': [],
        'error': None,
        'tool_count': 0
    }
    
    try:
        client = create_mcp_client(command, args)
        
        with client:
            mcp_tools = client.list_tools_sync()
            result['success'] = True
            result['tool_count'] = len(mcp_tools)
            
            # Get tool information
            for tool in mcp_tools:
                tool_info = get_tool_info(tool)
                result['tools'].append(tool_info)
                
    except ConnectionError as e:
        result['error'] = f"Connection failed: {e}"
    except ImportError as e:
        result['error'] = f"Missing dependency: {e}"
    except TimeoutError as e:
        result['error'] = f"Server timeout: {e}"
    except Exception as e:
        result['error'] = f"Unexpected error: {e}"
    
    return result


# MCP server configurations
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
        ],
        "env": {
            "AWS_DEFAULT_REGION": "us-east-1",
            "AWS_REGION": "us-east-1"
        }
    }
]