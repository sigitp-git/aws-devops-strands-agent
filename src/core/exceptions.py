#!/usr/bin/env python3
"""
Custom exceptions for AWS DevOps agent.
"""


class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass


class MCPConnectionError(AgentError):
    """Raised when MCP server connection fails."""
    
    def __init__(self, server_name: str, original_error: Exception):
        self.server_name = server_name
        self.original_error = original_error
        super().__init__(f"Failed to connect to {server_name}: {original_error}")


class MCPToolLoadError(AgentError):
    """Raised when MCP tools cannot be loaded."""
    
    def __init__(self, server_name: str, tool_count: int, original_error: Exception):
        self.server_name = server_name
        self.tool_count = tool_count
        self.original_error = original_error
        super().__init__(f"Failed to load {tool_count} tools from {server_name}: {original_error}")


class AgentTimeoutError(AgentError):
    """Raised when agent response times out."""
    
    def __init__(self, timeout_seconds: int):
        self.timeout_seconds = timeout_seconds
        super().__init__(f"Agent response timed out after {timeout_seconds} seconds")


class ConfigurationError(AgentError):
    """Raised when configuration is invalid or missing."""
    pass