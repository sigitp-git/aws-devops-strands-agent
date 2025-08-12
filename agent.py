# Import Agent and tools
import logging
import os

from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException
from strands.agent import Agent
from strands.tools import tool
from strands.models.bedrock import BedrockModel

# Set AWS region
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# Configure logging
logging.getLogger("strands").setLevel(
    logging.INFO
)  # Set to DEBUG for more detailed logs


# Define a websearch tool
@tool
def websearch(
    keywords: str, region: str = "us-en", max_results: int | None = None
) -> str:
    """Search the web to get updated information.
    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
        max_results (int | None): The maximum number of results to return.
    Returns:
        List of dictionaries with search results.
    """
    try:
        results = DDGS().text(keywords, region=region, max_results=max_results)
        return results if results else "No results found."
    except RatelimitException:
        return "RatelimitException: Please try again after a short delay."
    except DDGSException as d:
        return f"DuckDuckGoSearchException: {d}"
    except Exception as e:
        return f"Exception: {e}"


# Create a Bedrock model instance with temperature control
# Temperature 0.3: Focused and consistent responses, ideal for technical accuracy
# Adjust temperature: 0.1-0.3 (very focused), 0.4-0.7 (balanced), 0.8-1.0 (creative)
model = BedrockModel(
    model_id='us.anthropic.claude-sonnet-4-20250514-v1:0', 
    temperature=0.3
)

# Create an example agent
agent = Agent(
    model=model,
    system_prompt="""You are AWS DevOps bot, a helpful devops assistant for Amazon Web Services (AWS) environment.
    Help users find AWS DevOps best practices and answer questions related to AWS infrastructure development and operations.
    Use the websearch tool to find answers and best practices when users mention a topic or to look up specific AWS development and operations information.""",
    tools=[websearch],
)


if __name__ == "__main__":
    print("\n🚀 AWS-DevOps-bot: Ask me about DevOps on AWS! Type 'exit' to quit.\n")

    # Run the agent in a loop for interactive conversation
    while True:
        user_input = input("\nYou > ")
        if user_input.lower() == "exit":
            print("Happy DevOpsing!")
            break
        if not user_input.strip():
            print("\nAWS-DevOps-bot > Please ask me something about DevOps on AWS!")
            continue
        response = agent(user_input)
        print(f"\nAWS-DevOps-bot > {response}")