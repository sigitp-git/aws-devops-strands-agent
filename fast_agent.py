#!/usr/bin/env python3
"""
Ultra-fast AWS DevOps agent - knowledge only, no external tools.
"""

import logging
import sys
from typing import Optional

from strands.agent import Agent
from strands.models.bedrock import BedrockModel
from config import MODEL_ID, MODEL_TEMPERATURE


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


def extract_response_content(response) -> str:
    """Extract content from agent response with proper type handling."""
    if hasattr(response, 'content'):
        return response.content
    elif hasattr(response, 'text'):
        return response.text
    elif hasattr(response, 'message'):
        return response.message
    else:
        return str(response)


def validate_user_input(user_input: str) -> tuple[bool, Optional[str]]:
    """Validate user input with length and content checks."""
    if not user_input or not user_input.strip():
        return False, "Empty input"
    
    if len(user_input.strip()) > 1000:  # Reasonable limit
        return False, "Input too long (max 1000 characters)"
    
    # Check for potentially problematic characters
    if any(char in user_input for char in ['\x00', '\x01', '\x02']):
        return False, "Invalid characters in input"
    
    return True, None


class FastAgent:
    """Ultra-fast AWS DevOps agent with knowledge-only responses."""
    
    # Configuration constants
    EXIT_COMMANDS = ["exit", "quit", "bye"]
    WELCOME_MESSAGE = "⚡ Ultra-Fast AWS DevOps Bot (Knowledge Only)"
    HELP_MESSAGE = "💡 Instant responses - Type 'exit' to quit\n"
    EXIT_MESSAGE = "⚡ Fast DevOpsing!"
    PROCESSING_MESSAGE = "⚡ Instant response..."
    
    # Speed-optimized system prompt
    SYSTEM_PROMPT = """You are AWS DevOps bot. Answer AWS questions quickly from your knowledge.

SPEED RULES:
- Answer ONLY from built-in knowledge
- NO external tools or searches
- Keep responses under 150 words
- Be direct and practical"""
    
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
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return f"Sorry, I encountered an error: {e}"
    
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
                
                is_valid, error_msg = validate_user_input(user_input)
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