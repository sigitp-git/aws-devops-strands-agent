#!/usr/bin/env python3
"""
Configuration constants for AWS DevOps agent.
"""

import os
from dataclasses import dataclass
from typing import ClassVar
# Define a simple ConfigurationError here to avoid circular imports
class ConfigurationError(Exception):
    """Configuration-related error."""
    pass


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
    AGENT_TIMEOUT_SECONDS: ClassVar[int] = 30
    
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

CRITICAL EFFICIENCY RULES:
- Answer from knowledge FIRST before using tools
- Use tools ONLY when you need current/specific data
- MAXIMUM 1 tool call per response
- Keep responses under 300 words
- Be direct and actionable

NON-FUNCTIONAL RULES:
- Be friendly, patient, and understanding with customers
- Always offer additional help after answering questions
- If you can't help with something, direct customers to the appropriate contact
"""

# CLI Messages
WELCOME_MESSAGE = "\n🚀 AWS-DevOps-bot: Ask me about DevOps on AWS!"
HELP_MESSAGE = "💡 Type 'tools' to see available capabilities, or 'exit' to quit.\n"
EXIT_MESSAGE = "Happy DevOpsing!"
EMPTY_INPUT_MESSAGE = "\nAWS-DevOps-bot > Please ask me something about DevOps on AWS!"
PROCESSING_MESSAGE = "🤖 Processing your request..."

# Tool Commands
TOOL_COMMANDS = ["list tools", "show tools", "available tools", "what tools", "tools"]
EXIT_COMMANDS = ["exit", "quit", "bye"]


@dataclass(frozen=True)
class FastAgentConfig:
    """Fast agent specific configuration."""
    EXIT_COMMANDS: ClassVar[list[str]] = ["exit", "quit", "bye"]
    WELCOME_MESSAGE: ClassVar[str] = "⚡ Ultra-Fast AWS DevOps Bot (Knowledge Only)"
    HELP_MESSAGE: ClassVar[str] = "💡 Instant responses - Type 'exit' to quit\n"
    EXIT_MESSAGE: ClassVar[str] = "⚡ Fast DevOpsing!"
    PROCESSING_MESSAGE: ClassVar[str] = "⚡ Instant response..."
    EMPTY_INPUT_MESSAGE: ClassVar[str] = "AWS-DevOps-bot > Ask me about AWS DevOps!"
    MAX_INPUT_LENGTH: ClassVar[int] = 1000


@dataclass(frozen=True)
class EnvironmentConfig:
    """Environment validation and setup."""
    
    @classmethod
    def validate_aws_credentials(cls) -> bool:
        """Check if AWS credentials are available."""
        try:
            import boto3
            session = boto3.Session()
            credentials = session.get_credentials()
            return credentials is not None
        except Exception:
            return False
    
    @classmethod
    def validate_bedrock_access(cls) -> bool:
        """Validate Bedrock model access."""
        try:
            import boto3
            client = boto3.client('bedrock', region_name=AWSConfig.DEFAULT_REGION)
            # This is a lightweight check - just verify we can create the client
            return True
        except Exception:
            return False


def validate_environment() -> list[str]:
    """Validate environment setup and return any issues."""
    issues = []
    
    if not EnvironmentConfig.validate_aws_credentials():
        issues.append("AWS credentials not configured")
    
    if not EnvironmentConfig.validate_bedrock_access():
        issues.append("Cannot access AWS Bedrock service")
    
    return issues