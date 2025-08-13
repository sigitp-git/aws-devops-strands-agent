#!/usr/bin/env python3
"""
Configuration constants for AWS DevOps agent.
"""

import os
from dataclasses import dataclass
from typing import ClassVar
from exceptions import ConfigurationError


@dataclass(frozen=True)
class AWSConfig:
    """AWS-related configuration."""
    DEFAULT_REGION: ClassVar[str] = 'us-east-1'
    
    @classmethod
    def setup_environment(cls) -> None:
        """Set up AWS environment variables."""
        os.environ['AWS_DEFAULT_REGION'] = cls.DEFAULT_REGION


@dataclass(frozen=True)
class ModelConfig:
    """Model configuration with validation."""
    MODEL_ID: ClassVar[str] = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
    MODEL_TEMPERATURE: ClassVar[float] = 0.3
    
    @classmethod
    def validate(cls) -> None:
        """Validate model configuration."""
        if not (0.0 <= cls.MODEL_TEMPERATURE <= 1.0):
            raise ConfigurationError(
                f"MODEL_TEMPERATURE must be between 0.0 and 1.0, got {cls.MODEL_TEMPERATURE}"
            )
        
        if not cls.MODEL_ID:
            raise ConfigurationError("MODEL_ID cannot be empty")


@dataclass(frozen=True)
class TimeoutConfig:
    """Timeout configuration with validation."""
    SEARCH_TIMEOUT_SECONDS: ClassVar[int] = 10
    AGENT_TIMEOUT_SECONDS: ClassVar[int] = 45
    
    @classmethod
    def validate(cls) -> None:
        """Validate timeout configuration."""
        if cls.AGENT_TIMEOUT_SECONDS <= 0:
            raise ConfigurationError(
                f"AGENT_TIMEOUT_SECONDS must be positive, got {cls.AGENT_TIMEOUT_SECONDS}"
            )
        
        if cls.SEARCH_TIMEOUT_SECONDS <= 0:
            raise ConfigurationError(
                f"SEARCH_TIMEOUT_SECONDS must be positive, got {cls.SEARCH_TIMEOUT_SECONDS}"
            )


def validate_configuration() -> None:
    """Validate all configuration values."""
    ModelConfig.validate()
    TimeoutConfig.validate()


# Initialize configuration
AWSConfig.setup_environment()
validate_configuration()

# Backward compatibility - expose constants at module level
AWS_DEFAULT_REGION = AWSConfig.DEFAULT_REGION
MODEL_ID = ModelConfig.MODEL_ID
MODEL_TEMPERATURE = ModelConfig.MODEL_TEMPERATURE
SEARCH_TIMEOUT_SECONDS = TimeoutConfig.SEARCH_TIMEOUT_SECONDS
AGENT_TIMEOUT_SECONDS = TimeoutConfig.AGENT_TIMEOUT_SECONDS

# Search Configuration
DEFAULT_MAX_SEARCH_RESULTS = 3
MAX_SEARCH_RESULTS_LIMIT = 5

# System Prompt
SYSTEM_PROMPT = """You are AWS DevOps bot. Help with AWS infrastructure and operations.

GUIDELINES:
- Use AWS tools for specific queries (EKS, documentation, knowledge base)
- Keep responses concise and actionable
- Limit to 1 tool call per response
- Summarize long tool outputs into key points"""

# CLI Messages
WELCOME_MESSAGE = "\n🚀 AWS-DevOps-bot: Ask me about DevOps on AWS!"
HELP_MESSAGE = "💡 Type 'tools' to see available capabilities, or 'exit' to quit.\n"
EXIT_MESSAGE = "Happy DevOpsing!"
EMPTY_INPUT_MESSAGE = "\nAWS-DevOps-bot > Please ask me something about DevOps on AWS!"
PROCESSING_MESSAGE = "🤖 Processing your request..."

# Tool Commands
TOOL_COMMANDS = ["list tools", "show tools", "available tools", "what tools", "tools"]
EXIT_COMMANDS = ["exit", "quit", "bye"]