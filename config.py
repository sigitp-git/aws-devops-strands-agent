#!/usr/bin/env python3
"""
Configuration constants for AWS DevOps agent.
"""

import os

# AWS Configuration
AWS_DEFAULT_REGION = 'us-east-1'
os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION

# Model Configuration
MODEL_ID = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
MODEL_TEMPERATURE = 0.3

# Timeout Configuration
SEARCH_TIMEOUT_SECONDS = 10
AGENT_TIMEOUT_SECONDS = 30

# Search Configuration
DEFAULT_MAX_SEARCH_RESULTS = 3
MAX_SEARCH_RESULTS_LIMIT = 5

# System Prompt
SYSTEM_PROMPT = """You are AWS DevOps bot, a helpful devops assistant for Amazon Web Services (AWS) environment.
Help users find AWS DevOps best practices and answer questions related to AWS infrastructure development and operations.

TOOL USAGE GUIDELINES:
- You have access to powerful AWS tools including EKS cluster management, AWS documentation, and knowledge base access
- When users ask for specific AWS resource information (like "list my EKS clusters"), USE the appropriate tools to provide real data
- For EKS/Kubernetes questions, use the EKS MCP tools to provide actual cluster information and operations
- For AWS documentation queries, use the AWS Documentation or Knowledge tools
- For general questions, you can answer from your knowledge base
- Limit to 1 tool call per response for efficiency
- If a tool fails, provide helpful guidance based on your knowledge
- Keep responses concise and actionable"""

# CLI Messages
WELCOME_MESSAGE = "\n🚀 AWS-DevOps-bot: Ask me about DevOps on AWS!"
HELP_MESSAGE = "💡 Type 'tools' to see available capabilities, or 'exit' to quit.\n"
EXIT_MESSAGE = "Happy DevOpsing!"
EMPTY_INPUT_MESSAGE = "\nAWS-DevOps-bot > Please ask me something about DevOps on AWS!"
PROCESSING_MESSAGE = "🤖 Processing your request..."

# Tool Commands
TOOL_COMMANDS = ["list tools", "show tools", "available tools", "what tools", "tools"]
EXIT_COMMANDS = ["exit", "quit", "bye"]