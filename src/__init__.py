"""
AWS DevOps Strands Agent - Source Package

An intelligent AWS DevOps assistant bot built with the Strands Agents framework,
powered by Claude Sonnet 4 on AWS Bedrock with comprehensive MCP integration.

This package provides:
- Core agent functionality with dual performance modes
- MCP integration for AWS Documentation, Knowledge Base, and EKS
- Web search capabilities with DuckDuckGo integration
- Interactive CLI interface for technical consultations
"""

__version__ = "1.0.0"
__author__ = "AWS DevOps Team"
__description__ = "Intelligent AWS DevOps assistant with Strands Agents framework"

# Public API - define what gets imported with "from src import *"
__all__ = [
    # Core modules that should be publicly accessible
    "core",
    "interfaces", 
    "tools",
    "utils",
]

# Package metadata for introspection
__package_info__ = {
    "name": "aws-devops-strands-agent",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "python_requires": ">=3.10",
    "framework": "strands-agents",
    "model": "claude-sonnet-4",
    "aws_region": "us-east-1",
}