#!/usr/bin/env python3
"""
CLI interface utilities for AWS DevOps agent.
"""

import signal
from typing import List, Dict, Any
from config.config import (
    TOOL_COMMANDS, EXIT_COMMANDS, WELCOME_MESSAGE, HELP_MESSAGE,
    EXIT_MESSAGE, EMPTY_INPUT_MESSAGE, PROCESSING_MESSAGE,
    AGENT_TIMEOUT_SECONDS
)


class TimeoutHandler:
    """Context manager for handling timeouts."""
    
    def __init__(self, timeout_seconds: int, timeout_message: str):
        self.timeout_seconds = timeout_seconds
        self.timeout_message = timeout_message
        self.old_handler = None
    
    def __enter__(self):
        def timeout_handler(signum, frame):
            raise TimeoutError(self.timeout_message)
        
        self.old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(self.timeout_seconds)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)  # Cancel timeout
        if self.old_handler:
            signal.signal(signal.SIGALRM, self.old_handler)


def display_welcome():
    """Display welcome message."""
    print(WELCOME_MESSAGE)
    print(HELP_MESSAGE)


def display_tools_info(tools_count: int, mcp_tool_info: List[Dict[str, Any]]):
    """Display available tools information."""
    print(f"\n🛠️  Available Tools ({tools_count} total):")
    print("=" * 60)
    
    # Show websearch tool first
    print("\n🔍 Web Search Tools:")
    print("  1. websearch - Search the web to get updated information quickly")
    
    # Group MCP tools by server
    aws_doc_tools = []
    aws_knowledge_tools = []
    aws_eks_tools = []
    
    for tool_info in mcp_tool_info:
        server = tool_info['server']
        name = tool_info['name']
        desc = tool_info['description']
        
        # Truncate long descriptions
        if len(desc) > 80:
            desc = desc[:77] + "..."
        
        tool_entry = f"  • {name} - {desc}"
        
        if 'Documentation' in server:
            aws_doc_tools.append(tool_entry)
        elif 'Knowledge' in server:
            aws_knowledge_tools.append(tool_entry)
        elif 'EKS' in server:
            aws_eks_tools.append(tool_entry)
    
    # Display MCP tools by category
    if aws_doc_tools:
        print(f"\n📚 AWS Documentation Tools ({len(aws_doc_tools)} tools):")
        for tool in aws_doc_tools:
            print(tool)
    
    if aws_knowledge_tools:
        print(f"\n🧠 AWS Knowledge Tools ({len(aws_knowledge_tools)} tools):")
        for tool in aws_knowledge_tools:
            print(tool)
    
    if aws_eks_tools:
        print(f"\n☸️  AWS EKS Tools ({len(aws_eks_tools)} tools):")
        for tool in aws_eks_tools:
            print(tool)
    
    print("\n💡 You can ask me to use any of these tools or just ask questions naturally!")
    print("🎯 Example: 'Use AWS Documentation to find S3 pricing' or 'List my EKS clusters'")


def handle_user_input(user_input: str, agent: 'Agent', tools_count: int, mcp_tool_info: List[Dict[str, Any]]) -> bool:
    """
    Handle user input and return whether to continue the loop.
    
    Returns:
        bool: True to continue, False to exit
    """
    # Check for exit commands
    if user_input.lower() in EXIT_COMMANDS:
        print(EXIT_MESSAGE)
        return False
    
    # Check for empty input
    if not user_input.strip():
        print(EMPTY_INPUT_MESSAGE)
        return True
    
    # Check for tools command
    if user_input.lower() in TOOL_COMMANDS:
        display_tools_info(tools_count, mcp_tool_info)
        return True
    
    # Process agent request with timeout
    try:
        with TimeoutHandler(AGENT_TIMEOUT_SECONDS, "Agent response timeout"):
            print(PROCESSING_MESSAGE)
            response = agent(user_input)
            # Handle AgentResult object properly
            if hasattr(response, 'content'):
                print(f"\nAWS-DevOps-bot > {response.content}")
            else:
                print(f"\nAWS-DevOps-bot > {response}")
    except TimeoutError:
        print(f"\nAWS-DevOps-bot > I apologize, but that request took too long to process. "
              f"Let me provide a quick response based on my knowledge instead.")
    except Exception as e:
        print(f"\nAWS-DevOps-bot > I encountered an error: {e}. "
              f"Let me help you with general AWS DevOps guidance instead.")
    
    return True


def run_interactive_loop(agent: 'Agent', tools_count: int, mcp_tool_info: List[Dict[str, Any]]) -> None:
    """
    Run the main interactive CLI loop with MCP tools available.
    
    Args:
        agent: The configured agent instance
        tools_count: Total number of available tools
        mcp_tool_info: Information about MCP tools for display
    """
    display_welcome()
    
    while True:
        user_input = input("\nYou > ")
        should_continue = handle_user_input(user_input, agent, tools_count, mcp_tool_info)
        if not should_continue:
            break


def run_fallback_loop(agent: 'Agent', tools_count: int) -> None:
    """
    Run CLI loop without MCP tools (fallback mode).
    
    Args:
        agent: The configured agent instance
        tools_count: Total number of available tools (should be 1 for websearch only)
    """
    display_welcome()
    
    while True:
        user_input = input("\nYou > ")
        
        # Check for exit commands
        if user_input.lower() in EXIT_COMMANDS:
            print(EXIT_MESSAGE)
            break
        
        # Check for empty input
        if not user_input.strip():
            print(EMPTY_INPUT_MESSAGE)
            continue
        
        # Check for tools command
        if user_input.lower() in TOOL_COMMANDS:
            print(f"\n🛠️  Available Tools ({tools_count} total):")
            print("=" * 50)
            print("\n🔍 Web Search Tools:")
            print("  1. websearch - Search the web to get updated information quickly.")
            print("\n⚠️  Note: MCP servers (AWS Documentation, Knowledge, EKS) are not available.")
            print("💡 You can still ask me AWS DevOps questions and I'll help with my built-in knowledge!")
            continue
        
        # Process agent request with timeout
        try:
            with TimeoutHandler(AGENT_TIMEOUT_SECONDS, "Agent response timeout"):
                print(PROCESSING_MESSAGE)
                response = agent(user_input)
                # Handle AgentResult object properly
                if hasattr(response, 'content'):
                    print(f"\nAWS-DevOps-bot > {response.content}")
                else:
                    print(f"\nAWS-DevOps-bot > {response}")
        except TimeoutError:
            print(f"\nAWS-DevOps-bot > I apologize, but that request took too long to process. "
                  f"Let me provide a quick response based on my knowledge instead.")
        except Exception as e:
            print(f"\nAWS-DevOps-bot > I encountered an error: {e}. "
                  f"Let me help you with general AWS DevOps guidance instead.")