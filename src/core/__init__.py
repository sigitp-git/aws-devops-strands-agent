"""
Core application components for AWS DevOps agent.

This module provides the main entry points and core functionality for the AWS DevOps
Strands Agent, including agent implementations, MCP management, logging configuration,
and exception handling.

Components:
    - Agent creation and management (agent.py)
    - Fast knowledge-only agent (fast_agent.py) 
    - MCP client lifecycle management (mcp_manager.py)
    - Custom exception hierarchy (exceptions.py)
    - Structured logging configuration (logger.py)

Example:
    >>> from src.core import create_agent, FastAgent
    >>> agent, tool_count, mcp_info, clients = create_agent()
    >>> fast_agent = FastAgent()
"""

from .agent import create_agent, main as agent_main
from .fast_agent import FastAgent, main as fast_main
from .exceptions import (
    AgentError,
    AgentTimeoutError,
    ConfigurationError,
    MCPConnectionError,
    MCPToolLoadError,
)
from .logger import app_logger, cli_logger, mcp_logger
from .mcp_manager import MCPManager

__all__ = [
    # Agent components
    "create_agent",
    "agent_main",
    "FastAgent",
    "fast_main",
    "MCPManager",
    # Exception hierarchy (base first, then specific)
    "AgentError",
    "ConfigurationError",
    "MCPConnectionError",
    "MCPToolLoadError",
    "AgentTimeoutError",
    # Logging components
    "app_logger",
    "cli_logger",
    "mcp_logger",
]