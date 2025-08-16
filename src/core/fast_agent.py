#!/usr/bin/env python3
"""
Ultra-fast AWS DevOps agent - knowledge only, no external tools.
"""

import logging
import sys
from typing import Optional

from strands.agent import Agent
from strands.models.bedrock import BedrockModel
from config.config import MODEL_ID, MODEL_TEMPERATURE


def setup_logging() -> None:
    """Configure logging for fast agent with proper formatting."""
    # Suppress verbose strands logging
    logging.getLogger("strands").setLevel(logging.WARNING)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def _get_text_from_item(item) -> str:
    """Extract text from various item types."""
    if isinstance(item, dict):
        return item.get('text', str(item))
    if hasattr(item, 'text'):
        return str(item.text)
    return str(item)


def extract_response_content(response) -> str:
    """Extract content from agent response with simplified logic."""
    # Handle AgentResult with message attribute
    if hasattr(response, 'message') and isinstance(response.message, dict):
        content = response.message.get('content', [])
        if isinstance(content, list) and content:
            return _get_text_from_item(content[0])
    
    # Handle direct content attribute
    if hasattr(response, 'content'):
        content = response.content
        if isinstance(content, list) and content:
            return _get_text_from_item(content[0])
        return _get_text_from_item(content)
    
    # Handle direct text attributes
    for attr in ['text', 'message']:
        if hasattr(response, attr):
            return str(getattr(response, attr))
    
    # Handle dict response
    if isinstance(response, dict):
        if 'content' in response:
            content = response['content']
            if isinstance(content, list) and content:
                return _get_text_from_item(content[0])
            return _get_text_from_item(content)
        if 'text' in response:
            return str(response['text'])
    
    return str(response)


def validate_user_input(user_input: str, max_length: int = 1000) -> tuple[bool, Optional[str]]:
    """Validate user input with comprehensive checks."""
    if not user_input or not user_input.strip():
        return False, "Empty input"
    
    cleaned_input = user_input.strip()
    
    if len(cleaned_input) > max_length:
        return False, f"Input too long (max {max_length} characters)"
    
    # Check for control characters (more comprehensive)
    if any(ord(char) < 32 and char not in '\t\n\r' for char in cleaned_input):
        return False, "Invalid control characters in input"
    
    return True, None


class FastAgent:
    """Ultra-fast AWS DevOps agent with knowledge-only responses."""
    
    # Configuration constants
    MAX_RESPONSE_WORDS = 150
    MAX_INPUT_LENGTH = 1000
    MAX_ERROR_MESSAGE_LENGTH = 100
    QUERY_TIMEOUT_SECONDS = 30
    EXIT_COMMANDS = ["exit", "quit", "bye"]
    
    # UI Messages
    WELCOME_MESSAGE = "⚡ Ultra-Fast AWS DevOps Bot (Knowledge Only)"
    HELP_MESSAGE = "💡 Instant responses - Type 'exit' to quit\n"
    EXIT_MESSAGE = "⚡ Fast DevOpsing!"
    PROCESSING_MESSAGE = "⚡ Instant response..."
    
    # Speed-optimized system prompt
    SYSTEM_PROMPT = f"""You are AWS DevOps bot. Answer AWS questions quickly from your knowledge.

SPEED RULES:
- Answer ONLY from built-in knowledge
- NO external tools or searches
- Keep responses under {MAX_RESPONSE_WORDS} words
- Be direct and practical

NON-FUNCTIONAL RULES:
- Be friendly, patient, and understanding with customers
- Always offer additional help after answering questions
- If you can't help with something, direct customers to the appropriate contact"""
    
    def __init__(self):
        """Initialize the fast agent."""
        self.logger = logging.getLogger(__name__)
        try:
            self.model = BedrockModel(model_id=MODEL_ID, temperature=MODEL_TEMPERATURE)
            self.agent = Agent(model=self.model, system_prompt=self.SYSTEM_PROMPT, tools=[])
            self.logger.info("Fast agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize fast agent: {e}")
            raise
    
    def process_query(self, user_input: str) -> str:
        """Process user query and return response."""
        try:
            response = self.agent(user_input)
            return extract_response_content(response)
        except TimeoutError as e:
            self.logger.error(f"Query timeout: {e}")
            return "⚡ Response timeout - please try a simpler query"
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            error_msg = str(e)
            if len(error_msg) > self.MAX_ERROR_MESSAGE_LENGTH:
                error_msg = error_msg[:self.MAX_ERROR_MESSAGE_LENGTH] + "..."
            return f"⚡ Sorry, I encountered an error: {error_msg}"
    
    def run_interactive_loop(self) -> None:
        """Run the interactive command loop."""
        print(self.WELCOME_MESSAGE)
        print(self.HELP_MESSAGE)
        
        while True:
            try:
                user_input = input("You > ").strip()
                
                if user_input.lower() in self.EXIT_COMMANDS:
                    print(self.EXIT_MESSAGE)
                    break
                
                is_valid, error_msg = validate_user_input(user_input, self.MAX_INPUT_LENGTH)
                if not is_valid:
                    print(f"AWS-DevOps-bot > {error_msg}")
                    continue
                
                print(self.PROCESSING_MESSAGE)
                response = self.process_query(user_input)
                print(f"AWS-DevOps-bot > {response}")
                
            except KeyboardInterrupt:
                print(f"\n{self.EXIT_MESSAGE}")
                break
            except EOFError:
                print(f"\n{self.EXIT_MESSAGE}")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {e}")
                print(f"AWS-DevOps-bot > Unexpected error: {e}")


def main() -> int:
    """Main entry point for the fast agent."""
    setup_logging()
    
    try:
        agent = FastAgent()
        agent.run_interactive_loop()
        return 0
    except Exception as e:
        print(f"❌ Failed to start fast agent: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())