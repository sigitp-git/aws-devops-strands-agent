#!/usr/bin/env python3
"""
AWS DevOps Strands Agent - Main Entry Point

Full-featured agent with all capabilities including MCP integration.

This entry point provides access to the complete agent with all tools:
- Web search capabilities
- AWS Documentation access via MCP
- AWS Knowledge Base integration
- EKS cluster management tools

Usage:
    python3 main.py

Requirements:
    - AWS credentials configured
    - uv/uvx installed for MCP servers
    - Internet connection for web search and MCP tools
"""

import sys
import os
from pathlib import Path

def setup_path() -> None:
    """Add src directory to Python path for module imports."""
    src_path = Path(__file__).parent / 'src'
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

def main() -> int:
    """Main entry point with proper error handling."""
    try:
        setup_path()
        from core.agent import main as agent_main
        agent_main()
        return 0
    except ImportError as e:
        print(f"❌ Failed to import required modules: {e}")
        print("💡 Make sure you're running from the project root directory")
        print("💡 Install dependencies with: pip install -r requirements.txt")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Check your AWS credentials and configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())